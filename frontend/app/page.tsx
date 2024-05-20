"use client";
import { useState } from 'react';
import axios from 'axios';

const Home: React.FC = () => {
    const [message, setMessage] = useState<string>('');
    const [response, setResponse] = useState<string>('');

    const sendMessage = async () => {
        try {
            const res = await axios.post('http://localhost:8000/api/chat', { message });
            setResponse(res.data.reply);
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    return (
        <div>
            <h1>Chat Application</h1>
            <input 
                type="text" 
                value={message} 
                onChange={(e) => setMessage(e.target.value)} 
                placeholder="Type your message"
            />
            <button onClick={sendMessage}>Send</button>
            <p>Response: {response}</p>
        </div>
    );
}

export default Home;
