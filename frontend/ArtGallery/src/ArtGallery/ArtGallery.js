import React, { useState, useCallback, useEffect } from "react";
import ScrollLock from "react-scrolllock";
import { getArtById } from "../api/artService";

import { Nav } from "./Nav/Nav";
import { Gallery } from "./Gallery/Gallery";
import { FloatingArrow } from "./FloatingArrow/FloatingArrow";
import { ZoomCardItem } from "./ZoomCardItem/ZoomCardItem";

import "./art-gallery.css";

export const ArtGallery = (props) => {
  const [lock, setLock] = useState(false);
  const [search, setSearch] = useState("");
  const [card, setCard] = useState([]);
  const [wide, setWide] = useState(false);

  useEffect(() => {
    if (props.windowWidth < 501) {
      console.log("narrow");
      setWide(false);
    } else {
      console.log("wide");
      setWide(true);
    }
  }, [props.windowWidth]);

  const recieveNavSearchText = useCallback((props) => {
    setSearch(props);
  }, []);

  const recieveTagSearchText = useCallback((props) => {
    setLock(false);
    setSearch(props.toLowerCase());
  }, []);

  const recieveCardDetails = useCallback((propsChild) => {
    let cardId = propsChild.id;
    console.log("from recieveCardDetails", cardId);
    recieveCardFromDB(cardId);
  }, []);

  async function recieveCardFromDB(cardId) {
    try {
      let card = await getArtById(cardId);

      // Ensure image_url is well-formed
      card.image_url = card.image_url?.startsWith("http")
        ? card.image_url
        : `http://127.0.0.1:5000${card.image_url}`;

      setCard(card);
      setLock(true);
    } catch (err) {
      console.error("Failed to fetch card from backend:", err);
    }
  }

  return (
    <div id="ArtGallery" className="wide-art-gallery">
      <div
        className={
          lock
            ? wide
              ? "art-gallery-background avoid-clicks"
              : "art-gallery-background avoid-clicks no-scroll"
            : ""
        }
      >
        <Nav search={search} handleNavSearch={recieveNavSearchText} />
        <Gallery
          search={search}
          handleGalleryClickedCard={recieveCardDetails}
        />
        {wide && lock && <ScrollLock />}
      </div>

      {card === undefined || card.length === 0 || !lock ? (
        <FloatingArrow />
      ) : (
        <div className={wide ? "zoom-card-wide" : "zoom-card-narrow"}>
          <i
            className="fas fa-times exit-icon"
            onClick={() => setLock(false)}
          />
          <ZoomCardItem card={card} handleTagSearch={recieveTagSearchText} />
        </div>
      )}
    </div>
  );
};
