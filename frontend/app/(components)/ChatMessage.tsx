import React from 'react';

interface ChatMessageProps {
    message: string;
    sender: 'user' | 'bot';
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, sender }) => {
    return (
        <section className=''>
            <div className={`my-2 ${sender === 'user' ? 'flex justify-end' : 'flex justify-start'}`}>
                <div className={`p-4 rounded-lg ${sender === 'user' ? 'bg-zinc-800 text-white' : ' w-full'}`}>
                    <p className="text-left"><strong>{sender === 'user' ? 'You' : 'Bot'}:</strong> {message}</p>
                </div>
            </div>
        </section>
    );
};

export default ChatMessage;
