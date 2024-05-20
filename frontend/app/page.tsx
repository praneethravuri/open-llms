"use client";
import ChatWindow from "./(components)/ChatWindow";

const Home: React.FC = () => {
    return (
        <div>
            <h1>Chat with GPT-2</h1>
            <ChatWindow />
        </div>
    );
}

export default Home;