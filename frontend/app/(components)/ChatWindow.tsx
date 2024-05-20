"use client";
import { useState } from 'react';
import axios from 'axios';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';

const ChatWindow: React.FC = () => {
    const [messages, setMessages] = useState<{ sender: 'user' | 'bot'; message: string; }[]>([]);

    const sendMessage = async (message: string) => {
        setMessages([...messages, { sender: 'user', message }]);
        try {
            const response = await axios.post('http://localhost:8000/api/chat', { message }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            setMessages([...messages, { sender: 'user', message }, { sender: 'bot', message: response.data.reply }]);
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    return (
        <section className='p-10'>
            <div>
                {messages.map((msg, index) => (
                    <ChatMessage key={index} message={msg.message} sender={msg.sender} />
                ))}
            </div>
            <ChatInput onSendMessage={sendMessage} />
        </section>
    );
};

export default ChatWindow;
