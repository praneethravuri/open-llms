import React, { useState } from 'react';
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { ArrowUpFromLine } from 'lucide-react';

interface ChatInputProps {
    onSendMessage: (message: string) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage }) => {
    const [input, setInput] = useState<string>("");
    const [isButtonDisabled, setButtonDisabled] = useState(true);

    const handleSend = () => {
        if (input.trim() !== "") {
            console.log(input);
            onSendMessage(input);
            setInput("");
            setButtonDisabled(true);
        }
    };

    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        const inputValue = event.target.value;
        setInput(inputValue);
        setButtonDisabled(inputValue.trim() === "");
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (event.key === 'Enter') {
            handleSend();
        }
    };

    return (
        <section className="chat-input flex justify-center">
            <div className="input-area flex items-center justify-between bg-light-gray md:w-[calc(100%)] w-full space-x-4 p-5 rounded-lg">
                <div className='text-input w-full'>
                    <Textarea
                        rows={1}
                        className='bg-transparent resize-none w-full border-none'
                        placeholder='Enter a message'
                        value={input}
                        onChange={handleChange}
                        onKeyDown={handleKeyDown}
                    />
                </div>
                <div className="send-btn">
                    <Button disabled={isButtonDisabled} className='border-none' onClick={handleSend}>
                        <ArrowUpFromLine width={24} />
                    </Button>
                </div>
            </div>
        </section>
    );
}

export default ChatInput;