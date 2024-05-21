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
        <section className="fixed bottom-0 w-full py-4 flex justify-center">
            <div className="flex justify-center items-center w-full max-w-3xl ">
                <Textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    className="mr-4 bg-light-gray font-normal border-none ring-transparent text-white resize-none"
                />
                <Button onClick={handleSend} variant="secondary">
                    <ArrowUpFromLine />
                </Button>
            </div>
        </section>
    );
};

export default ChatInput;
