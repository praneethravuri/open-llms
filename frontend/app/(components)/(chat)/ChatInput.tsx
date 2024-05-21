"use client";

import { useState } from "react";

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
            onSendMessage(input);
            setInput("");
        }
    };

    return (
        <div className="fixed bottom-0 w-full p-4 mx-auto">
            <div className="flex justify-between w-full">
                <div className="flex justify-between w-10/12 items-center">
                    <Textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your message..."
                        className="mr-4 bg-light-gray font-normal rounded-lg border-none ring-transparent text-white resize-none"
                    />
                    <Button className=" pt-6 pb-6" onClick={handleSend} variant="secondary">
                        <ArrowUpFromLine />
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default ChatInput;