"use client";
import { useState } from "react";
import { Input } from "@/components/ui/input";
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
        <div className="fixed bottom-0 w-full flex justify-center p-4">
            <div className="flex items-center w-full max-w-3xl">
                <Input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    className="flex-grow mr-4 bg-light-gray font-normal border-none ring-transparent  text-white"
                />
                <Button onClick={handleSend} variant="secondary">
                    <ArrowUpFromLine />
                </Button>
            </div>
        </div>
    );
};

export default ChatInput;
