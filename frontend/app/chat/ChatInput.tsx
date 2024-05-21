"use client";
import React, { useState } from 'react';
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { ArrowUpFromLine } from 'lucide-react';

interface ChatInputProps {
    onSendMessage: (message: string) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage }) => {

    const [input, setInput] = useState<string>("");

    const handleSend = () => {
        if (input.trim() !== "") {
            console.log(input);
            onSendMessage(input);
            setInput("");
        }
    };

    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInput(event.target.value);
    };

    return (
        <section className="chat-input flex justify-center">
            <div className="input-area flex items-center justify-between bg-light-gray w-3/6 space-x-4 p-5 rounded-lg">
                <div className='text-input w-full'>
                    <Textarea
                        rows={1}
                        className='bg-transparent resize-none w-full border-none'
                        placeholder='Enter a message'
                        value={input}
                        onChange={handleChange}
                    />
                </div>
                <div className="send-btn">
                    <Button className='border-none' onClick={handleSend}>
                        <ArrowUpFromLine width={24} />
                    </Button>
                </div>
            </div>
        </section>
    );
}

export default ChatInput;
