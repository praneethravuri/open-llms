"use client";
import React, { useState } from 'react';
import { Copy, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ChatMessageProps {
    message: string;
    sender: 'user' | 'bot';
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, sender }) => {
    const [copied, setCopied] = useState<boolean>(false);

    const copyToClipboard = () => {
        navigator.clipboard.writeText(message).then(() => {
            setCopied(true);
        }, (err) => {
            alert("Failed to copy message");
        });
    };

    return (
        <section className='mb-20'>
            <div className={`my-2 ${sender === 'user' ? 'flex justify-end' : 'flex justify-start'}`}>
                <div className={`p-4 rounded-lg ${sender === 'user' ? 'bg-light-gray text-white' : 'w-full'}`}>
                    <p className="text-left">{message}</p>
                    {sender === 'bot' && (
                        <div className="flex justify-start mt-2">
                            <Button onClick={copyToClipboard} className="bg-very-dark-gray text-white rounded-lg text-sm flex space-x-2">
                                {copied ? <Check width={16} /> : <Copy width={16} />}
                                <p className='text-xs'>{copied ? 'Copied!' : 'Copy'}</p>
                            </Button>
                        </div>
                    )}
                </div>
            </div>
        </section>
    );
}

export default ChatMessage;
