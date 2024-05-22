"use client";
import React from 'react';
import { useParams } from 'next/navigation';
import ChatWindow from '@/app/chat/ChatWindow';

const ChatPage = () => {
    const { id } = useParams();

    return (
        <div >
            <ChatWindow />
        </div>
    );
};

export default ChatPage;
