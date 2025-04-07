import React from "react";
import "./card-item.css";

/**
 * Card component
 * @param {Card currentCard} props
 */
function Card(props) {
  const currentCard = props.currentCard;

  return (
    <div id="cardContainer" className="card-container card-border">
      <div className="card-image-container">
        <img
          id="cardImage"
          className="card-image"
          alt={currentCard.name}
          src={currentCard.image_url || "https://via.placeholder.com/300"}
        />
      </div>
      <div className="overlay">
        <div id="cardTitleContainer" className="items card-title-container">
          <p id="cardTitle">{currentCard.name}</p>
          <hr />
        </div>
        <div id="cardDateContainer" className="items card-date-container">
          <p id="cardDate">
            {currentCard.date_created?.split("T")[0] || "No Date"}
          </p>
        </div>
      </div>
    </div>
  );
}

export const CardItem = (props) => {
  function updateCardDetailsOnClick(e) {
    e.preventDefault();

    let card = props.currentCard;

    props.handleClickedCard(card);
  }

  return (
    <li onClick={updateCardDetailsOnClick}>
      <Card currentCard={props.currentCard} />
    </li>
  );
};
