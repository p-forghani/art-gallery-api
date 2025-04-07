import React, { useState, useEffect, useCallback } from "react";
import "./gallery.css";
import { CardItem } from "../CardItem/CardItem";
import { getAllArt } from "../../api/artService";

export const Gallery = (props) => {
  const [cardItemsData, setCardItemsData] = useState([]);
  const [clickedCard, setClickedCard] = useState([]);

  const recieveCardDetails = useCallback(
    (propsChild) => {
      let card = propsChild;
      console.log("🖼️ Clicked Card:", card);
      setClickedCard(card);
      props.handleGalleryClickedCard(card);
    },
    [props]
  );

  useEffect(() => {
    getAllArt()
      .then((data) => {
        const formattedData = {};
        data.forEach((item) => {
          console.log("📸 Image URL:", item.image_url); // Confirm backend value
          formattedData[item.id] = {
            ...item,
            image_url: item.image_url?.startsWith("http")
              ? item.image_url
              : `http://127.0.0.1:5000${item.image_url}`, // ensure correct URL
          };
        });
        setCardItemsData(formattedData);
      })
      .catch(console.error);
  }, []);

  let cardItemsList = createCardItemsList(
    props.search,
    cardItemsData,
    recieveCardDetails
  );

  return (
    <div id="galleryContainer" className="gallery-container">
      <ul id="gallery" className="gallery">
        {cardItemsList}
      </ul>
      <p id="cardsCounter" className="cards-counter">
        {cardItemsList.length} items found
      </p>
    </div>
  );
};

function createCardItemsList(search, cardItemsData, recieveCardDetails) {
  let values = Object.values(cardItemsData);
  let list;

  if (search) {
    list = filterCards(values, search);
  } else {
    list = values;
  }

  return list.map((i) => (
    <CardItem
      currentCard={i}
      key={i.id.toString()}
      handleClickedCard={recieveCardDetails}
    />
  ));
}

function filterCards(values, search) {
  return values.filter((i) => {
    const titleFlag = i.name.toLowerCase().includes(search);
    let tagsFlag = false;

    if (!titleFlag && i.tags) {
      tagsFlag = i.tags.some((tag) => tag.toLowerCase().includes(search));
    }

    return titleFlag || tagsFlag;
  });
}
