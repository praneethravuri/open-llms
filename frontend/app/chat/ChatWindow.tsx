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
} from "@/components/ui/select";

const ChatWindow = () => {
    const [messages, setMessages] = useState<{ sender: 'user' | 'bot'; message: string; }[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [selectedModel, setSelectedModel] = useState<string>("deepset/tinyroberta-squad2");
    const [serverStatus, setServerStatus] = useState<string>("offline");

    const modelList = [
        "deepset/tinyroberta-squad2",
        "sshleifer/distilbart-cnn-12-6",
        "deepset/roberta-base-squad2",
        "Intel/dynamic_tinybert",
        "distilbert/distilbert-base-cased-distilled-squad"
    ];

    const checkServerStatus = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/server-status');
            if (response.status === 200) {
                setServerStatus("online");
            } else {
                setServerStatus("offline");
            }
        } catch (error) {
            setServerStatus("offline");
        }
    };

    useEffect(() => {
        checkServerStatus(); // Initial check

        let interval: NodeJS.Timeout;
        if (serverStatus === "offline") {
            interval = setInterval(checkServerStatus, 5000); // Check every 5 seconds if offline
        }

        return () => {
            if (interval) {
                clearInterval(interval); // Clear interval on component unmount
            }
        };
    }, [serverStatus]);

    const sendMessage = async (message: string) => {
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:8000/api/ask', { question: message, model: selectedModel }, {
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
        <section className='h-screen flex flex-col items-center justify-center'>
            <main className='md:w-3/6 w-full h-full flex flex-col'>
                <div className="model-status-selection flex items-center justify-between p-4">
                    <div className="model-selection">
                        <Select value={selectedModel} onValueChange={setSelectedModel}>
                            <SelectTrigger className="w-[200px]">
                                <SelectValue placeholder="Select model" />
                            </SelectTrigger>
                            <SelectContent>
                                {modelList.map((model, index) => (
                                    <SelectItem key={index} value={model}>{model}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="server-status flex justify-end">
                        <Badge variant={serverStatus === "online" ? "online" : "offline"}>
                            Server {serverStatus === "online" ? "Online" : "Offline"}
                        </Badge>
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
                <div className="input-message p-4">
                    <ChatInput onSendMessage={sendMessage} />
                </div>
            </main>
        </section>
    );
}

export default ChatWindow;
