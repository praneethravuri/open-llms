"use client";

import React, { useState, useEffect } from 'react';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';
import axios from 'axios';
import Instruction from '@/components/static/Instruction';
import LoadingSpinner from '@/components/static/LoadingSpinner';
import { Badge } from "@/components/ui/badge";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"


const ChatWindow = () => {
    const [messages, setMessages] = useState<{ sender: 'user' | 'bot'; message: string; }[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [modelReady, setModelReady] = useState<boolean>(false);

    useEffect(() => {
        const checkModelReady = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/health');
                if (response.data.status === "ready") {
                    setModelReady(true);
                } else {
                    throw new Error("Model not ready");
                }
            } catch (error) {
                console.error("Model not ready yet:", error);
                setTimeout(checkModelReady, 5000);
            }
        };

        checkModelReady();
    }, []);

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
            <div className="model-status-selection flex items-center justify-between p-4">
                <div className="model-selection">
                    <Select>
                        <SelectTrigger className="w-[200px]">
                            <SelectValue placeholder="Select model" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="sshleifer/distilbart-cnn-12-6">sshleifer/distilbart-cnn-12-6</SelectItem>
                            <SelectItem value="sshleifer/distilbart-cnn-12-6">sshleifer/distilbart-cnn-12-6</SelectItem>
                            <SelectItem value="sshleifer/distilbart-cnn-12-6">sshleifer/distilbart-cnn-12-6</SelectItem>
                        </SelectContent>
                    </Select>

                </div>
                <div className="model-status flex justify-end">
                    {!modelReady ? (
                        <Badge variant="offline">Model Offline</Badge>
                    ) : (
                        <Badge variant="online">Model Online</Badge>
                    )}
                </div>
            </div>
            <div className="show-messages flex-grow overflow-auto p-4">
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
            <div className="input-message mb-10 p-4">
                <ChatInput onSendMessage={sendMessage} />
            </div>
        </section>
    )
}

export default ChatWindow;
