"use client";
import ChatWindow from "@/app/(components)/(chat)/ChatWindow";
import Sidebar from "@/app/(components)/(sidebar)/Sidebar";

const Home: React.FC = () => {
    return (
        <section className="h-screen w-full flex">
            <div className="w-1/6">
                <Sidebar />
            </div>
            <div className="w-5/6">
                <ChatWindow />
            </div>
        </section>
    );
}

export default Home;
