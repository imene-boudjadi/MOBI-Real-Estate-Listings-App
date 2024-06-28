import React, { createContext, useState } from "react";

export const ItemContext = createContext();

export const ItemProvider = ({ children }) => {
  const [clickedItem, setClickedItem] = useState(null);
  const [gEmail,setGEmail]=useState('');
  const [gName,setGName]=useState('');


  return (
    <ItemContext.Provider value={{ clickedItem, setClickedItem , gEmail, setGEmail,gName,setGName}}>
      {children}
    </ItemContext.Provider>
  );
};
