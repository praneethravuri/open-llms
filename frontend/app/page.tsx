"use client";
import ChatWindow from "./(components)/ChatWindow";
import Sidebar from "@/components/static/Sidebar";

const Home: React.FC = () => {
    return (
        <section className="h-screen w-full flex">
            <Sidebar />
            <div className="">
                <ChatWindow />
            </div>
        </section>
    );
}

export default Home;
