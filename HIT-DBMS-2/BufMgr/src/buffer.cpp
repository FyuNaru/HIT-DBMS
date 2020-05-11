/**
 * @author See Contributors.txt for code contributors and overview of BadgerDB.
 *
 * @section LICENSE
 * Copyright (c) 2012 Database Group, Computer Sciences Department, University of Wisconsin-Madison.
 */

#include <memory>
#include <iostream>
#include "buffer.h"
#include "exceptions/buffer_exceeded_exception.h"
#include "exceptions/page_not_pinned_exception.h"
#include "exceptions/page_pinned_exception.h"
#include "exceptions/bad_buffer_exception.h"
#include "exceptions/hash_not_found_exception.h"

namespace badgerdb { 

BufMgr::BufMgr(std::uint32_t bufs)
	: numBufs(bufs) {
	bufDescTable = new BufDesc[bufs];

  for (FrameId i = 0; i < bufs; i++) 
  {
  	bufDescTable[i].frameNo = i;
  	bufDescTable[i].valid = false;
  }

  bufPool = new Page[bufs];

	int htsize = ((((int) (bufs * 1.2))*2)/2)+1;
  hashTable = new BufHashTbl (htsize);  // allocate the buffer hash table

  clockHand = bufs - 1;
}


BufMgr::~BufMgr() {
	delete [] bufDescTable;
	delete [] bufPool;
	delete hashTable;
}

void BufMgr::advanceClock()
{
	clockHand = (clockHand + 1) % numBufs;
}

void BufMgr::allocBuf(FrameId & frame) 
{
	//record the time of pinned
	int pinCnt = 0;
	while(true){
		advanceClock();
		if(!bufDescTable[clockHand].valid){
			//the page in this frame is not valid
			frame = clockHand;
			return;
		} 
		else if(bufDescTable[clockHand].refbit){
			//the page in this frame is visited recently
			//clear refbit
			bufDescTable[clockHand].refbit = false;
			//reset the pinCnt
			pinCnt = 0;
			continue;
		}
		else if(bufDescTable[clockHand].pinCnt){
			//the page is pinned
			pinCnt++;
			if(pinCnt >= 100){
				//no more frames left for allocation
                throw BufferExceededException();
			}
			continue;
		}
		else if(bufDescTable[clockHand].dirty){
			//the page is dirty
			//flush page to disk
			bufDescTable[clockHand].file->writePage(bufPool[clockHand]);
			
		}
		//only need remove hashtable item
		//set and add hashtable item will be in the readPage() and allocPage()
		frame = clockHand;
		hashTable->remove(bufDescTable[clockHand].file, bufDescTable[clockHand].pageNo);
		bufDescTable[clockHand].Clear(); 
		return;
	}
}

	
void BufMgr::readPage(File* file, const PageId pageNo, Page*& page)
{
	FrameId frame;
	try{
		//find the page in the pool, and get the frameid
		hashTable->lookup(file, pageNo, frame);
		bufDescTable[frame].refbit = true;
		bufDescTable[frame].pinCnt++;
		page = bufPool + frame;
	}
	catch(HashNotFoundException e){
		//can't find the page in the pool
		//so fetch the page from file
		allocBuf(frame);
		bufPool[frame] = file->readPage(pageNo);
		hashTable->insert(file, pageNo, frame);
		bufDescTable[frame].Set(file, pageNo);
		page = bufPool + frame;
	}
}


void BufMgr::unPinPage(File* file, const PageId pageNo, const bool dirty) 
{
	FrameId frame;
	try{
		hashTable->lookup(file, pageNo, frame);
		if(bufDescTable[frame].pinCnt == 0){
			//the page is not pinned
			throw PageNotPinnedException(bufDescTable[frame].file->filename(), bufDescTable[frame].pageNo, frame);
		}
		else{
			//decrease the pinCnt
			bufDescTable[frame].pinCnt--;
			if(dirty == true){
				bufDescTable[frame].dirty = true;
			}
		}
	}
	catch(HashNotFoundException e){
		//can't find this page, do nothing
	}
}

void BufMgr::flushFile(const File* file) 
{
	for(FrameId i = 0; i < numBufs; i++){
		if(bufDescTable[i].file == file){
			if(!bufDescTable[i].valid){
				throw BadBufferException(i, bufDescTable[i].dirty, bufDescTable[i].valid, bufDescTable[i].refbit);
			}
			else if(bufDescTable[i].pinCnt > 0){
				throw PagePinnedException(file->filename(), bufDescTable[i].pageNo, i);
			}
			else if(bufDescTable[i].dirty){
				bufDescTable[i].file->writePage(bufPool[i]);
			}
			
			//remove from hashtable
			hashTable->remove(file, bufDescTable[i].pageNo);
			//clear
			bufDescTable[i].Clear();
		}
	}
}

void BufMgr::allocPage(File* file, PageId &pageNo, Page*& page) 
{
	//create a page and find a frame for it
	Page p = file->allocatePage();
	FrameId frame;
	allocBuf(frame);

	//put the page into frame and create a hashtable item
	bufPool[frame] = p;
	pageNo = p.page_number();
	hashTable->insert(file, pageNo, frame);
	
	//set
	bufDescTable[frame].Set(file, pageNo);

	page = bufPool + frame;
}

void BufMgr::disposePage(File* file, const PageId PageNo)
{
	FrameId frame;
	try{
		//if this page is in the bufPool
		//delete from hashtable
		hashTable->lookup(file, PageNo, frame);
		hashTable->remove(file, PageNo);
		//clear frame
		bufDescTable[frame].Clear();
	}
	catch(HashNotFoundException e){
		//do nothing
	}
	//delete page
	file->deletePage(PageNo);
}

void BufMgr::printSelf(void) 
{
  BufDesc* tmpbuf;
	int validFrames = 0;
  
  for (std::uint32_t i = 0; i < numBufs; i++)
	{
  	tmpbuf = &(bufDescTable[i]);
		std::cout << "FrameNo:" << i << " ";
		tmpbuf->Print();

  	if (tmpbuf->valid == true)
    	validFrames++;
  }

	std::cout << "Total Number of Valid Frames:" << validFrames << "\n";
}

}
