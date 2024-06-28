import React, { useContext } from 'react';
import { ItemContext } from "../Source/ItemProvider";
import "./maps.css";

const maps = () => {
const { clickedItem } = useContext(ItemContext);

  return (
    <div className="MapCommune">
      <iframe
        title="Localisation"
        src={`https://maps.google.com/maps?q=" +
            ${clickedItem.commune} +" "+ ${clickedItem.wilaya}
            "&t=&z=13&ie=UTF8&iwloc=&output=embed`}
        width="100%"
        height="100%"
        style={{ border: "0" }}
        allowFullScreen=""
        loading="lazy"
        referrerPolicy="no-referrer-when-downgrade"
      ></iframe>
    </div>
  );
};

export default maps;

