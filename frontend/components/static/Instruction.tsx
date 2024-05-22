import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const Instruction = () => {
    const instructions = [
        { title: "Select Model", content: "Choose a pre-trained language model from a curated list to get started." },
        { title: "Ask Your Question", content: "Enter your query and submit it to the selected model for a response." },
        { title: "Chat History", content: "Access your chat history to revisit past interactions and insights." },
    ];

    return (
        <section className=' h-full flex flex-col justify-center'>
            <div className="main-content flex flex-col justify-between space-y-8">
                <div className="sm:block hidden">
                    <div className="header flex justify-between sm:block">
                        <div className="title text-2xl font-semibold">How to get started</div>
                        <div className="instruction text-gray-text-color line-clamp-3">Here&lsquo;s a quick overview of the process, from start to finish</div>
                    </div>
                </div>
                <div className="instruction-cards grid gap-5 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                    {instructions.map((instruction, index) => (
                        <div key={index} className="break-inside-avoid cursor-default">
                            <Card className='bg-transparent border border-zinc-700 h-full'>
                                <CardHeader>
                                    <CardTitle className='flex justify-between'>
                                        <div className='font-medium text-xl mb-1 text-white'>{instruction.title}</div>
                                    </CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <p className='text-base text-gray-text-color'>{instruction.content}</p>
                                </CardContent>
                            </Card>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

export default Instruction;