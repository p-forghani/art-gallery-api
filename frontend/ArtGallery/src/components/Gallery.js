import React, { useEffect, useState } from 'react';
import { getAllArt } from '../api/artService';

const Gallery = () => {
  const [arts, setArts] = useState([]);

  useEffect(() => {
    getAllArt().then(setArts).catch(console.error);
  }, []);

  return (
    <div>
      <h1>Art Gallery</h1>
      {arts.map((art) => (
        <div key={art.id} style={{ margin: '20px', border: '1px solid #ccc', padding: '10px' }}>
          <h3>{art.name}</h3>
          <p>{art.description}</p>
          <p>Category ID: {art.category_id}</p>
          <p>Tag ID: {art.tag_id}</p>
          <p>Price: ${art.price}</p>
        </div>
      ))}
    </div>
  );
};

export default Gallery;
