import React, { useState, useEffect, useCallback } from "react";
import "./zoom-card-item.css";
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";

export const ZoomCardItem = (props) => {
  const card = props.card;
  const [search, setSearch] = useState("");

  const recieveTagText = useCallback((childProps) => {
    setSearch(childProps);
    props.handleTagSearch(childProps);
  }, [props]);

  const tagsList = createTagsList(card.tags || [], recieveTagText);

  return (
    <div className="zoom-container">
      <ZoomImage card={card} />
      <div id="detailsContainer" className="details-container">
        <p id="title" className="title">
          {card.name}
        </p>
        <hr />
        <p id="description">{card.description}</p>
        <p id="date" className="date">
          – {card.date_created?.split("T")[0]}
        </p>
        <ul>{tagsList}</ul>
      </div>
    </div>
  );
};

function createTagsList(tags, recieveTagText) {
  return tags.map((i) => (
    <Tag currentTag={i} key={i} handleTagSearch={recieveTagText} />
  ));
}

function Tag(props) {
  const [tag] = useState(props.currentTag.toString());

  function updateSearch(event) {
    event.preventDefault();
    props.handleTagSearch(tag);
  }

  return (
    <li className="tag" onClick={updateSearch}>
      #{tag}
    </li>
  );
}

function ZoomImage(props) {
  let card = props.card;
  return (
    <div id="imageContainer" className="image-container">
      <TransformWrapper>
        {({ zoomIn, zoomOut, resetTransform }) => (
          <React.Fragment>
            <div className="image-wrapper">
              <TransformComponent>
                <img
                  id="image"
                  className="image"
                  src={card.image_url || "https://via.placeholder.com/300"}
                  alt={card.name}
                />
              </TransformComponent>
            </div>
            <div className="tools">
              <button className="zoom-in-btn" onClick={zoomIn}>
                <i className="fas fa-search-plus zoom-in-icon" />
              </button>
              <button className="zoom-out-btn" onClick={zoomOut}>
                <i className="fas fa-search-minus zoom-out-icon" />
              </button>
              <button className="zoom-reset-btn" onClick={resetTransform}>
                <i className="fas fa-expand zoom-reset-icon" />
              </button>
            </div>
          </React.Fragment>
        )}
      </TransformWrapper>
    </div>
  );
}
