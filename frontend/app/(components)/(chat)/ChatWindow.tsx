"use client";
import React, { useState } from 'react';
import axios from 'axios';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';

const ChatWindow = () => {

    const [messages, setMessages] = useState<{ sender: 'user' | 'bot'; message: string; }[]>([]);

    const sendMessage = async (message: string) => {
        setMessages([...messages, { sender: 'user', message }]);
        try {
            const response = await axios.post('http://localhost:8000/api/ask', { question: message }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            setMessages([...messages, { sender: 'user', message }, { sender: 'bot', message: response.data.answer }]);
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    return (
        <div className='h-screen'>
            <div className=''>
                {messages.map((msg, index) => (
                    <ChatMessage key={index} message={msg.message} sender={msg.sender} />
                ))}
                <ChatInput onSendMessage={sendMessage} />
            </div>
        </div>
    )
}

export default ChatWindow