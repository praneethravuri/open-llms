"use client";

import React, { useState } from 'react';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';
import axios from 'axios';
import Instruction from '@/components/static/Instruction';
import LoadingSpinner from '@/components/static/LoadingSpinner';

const ChatWindow = () => {
    const [messages, setMessages] = useState<{ sender: 'user' | 'bot'; message: string; }[]>([]);
    const [loading, setLoading] = useState<boolean>(false);

    const sendMessage = async (message: string) => {
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:8000/api/ask', { question: message }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            setMessages((prevMessages) => [...prevMessages, { sender: 'user', message }, { sender: 'bot', message: response.data.answer }]);
        } catch (error) {
            console.error("Error sending message:", error);
            setMessages((prevMessages) => [...prevMessages, { sender: 'user', message }, { sender: 'bot', message: "Sorry, something went wrong. Please try again." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className='h-screen flex flex-col'>
            <div className="show-messages flex-grow overflow-auto">
                {messages.length === 0 ? (
                    <Instruction />
                ) : (
                    <>
                        {messages.map((msg, index) => (
                            <ChatMessage key={index} message={msg.message} sender={msg.sender} />
                        ))}
                        {loading && <LoadingSpinner />}
                    </>
                )}
            </div>
            <div className="input-message mb-10">
                <ChatInput onSendMessage={sendMessage} />
            </div>
        </section>
    )
}

export default ChatWindow;
