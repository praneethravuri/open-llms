import React from 'react';
import Sidebar from '@/components/Sidebar';
import ChatWindow from './ChatWindow';

const page = () => {
  return (
    <section className='bg-black h-screen w-full flex'>
        <Sidebar />
        <main className="main-content flex-1 px-20 py-8 bg-dark-gray">
            <div className="select-llm">

            </div>
            <div className="chat-area">
                <ChatWindow />
            </div>
        </main>
    </section>
  )
}

export default page