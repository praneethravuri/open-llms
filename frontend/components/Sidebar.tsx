"use client";

import { Button } from './ui/button';
import React, { useState } from 'react';
import { PanelLeftOpen, PanelRightOpen } from 'lucide-react';

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const toggleSidebar = () => {
    setIsOpen((prevIsOpen) => {
      const newIsOpen = !prevIsOpen;
      console.log(newIsOpen);
      return newIsOpen;
    });
  };
  const chatLinks = [
    { id: 1, text: 'Chat Link 1' },
    { id: 2, text: 'Chat Link 2' },
    { id: 3, text: 'Chat Link 3' },
    { id: 4, text: 'Chat Link 4' },
    { id: 5, text: 'Chat Link 5' },
  ];

  return (
    <section
      className={`xl:block overflow-y-auto h-screen w-1/6 px-4 py-8 bg-very-dark-gray ${isOpen ? 'block' : 'hidden'
        }`}
    >
      <div className="cursor-pointer mb-10" onClick={toggleSidebar}>
        {isOpen ? <PanelLeftOpen /> : <PanelRightOpen />}
      </div>
      <div className="chats space-y-4">
        {chatLinks.map((link) => (
          <div className="individual-chat w-full" key={link.id}>
            <Button className="chat-link p-1 m-0 w-full">
              <p className='text-sm'>{link.text}</p>
              <div></div>
            </Button>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Sidebar;