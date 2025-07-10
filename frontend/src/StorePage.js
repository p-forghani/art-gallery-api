import React, { useEffect, useState } from 'react';
import { getArtworks } from './api';
import { Container, Typography, Grid, Paper, CircularProgress, Alert } from '@mui/material';

const aspectRatios = [
  { h: 200, w: 200 },
  { h: 250, w: 180 },
  { h: 180, w: 250 },
  { h: 300, w: 200 },
  { h: 200, w: 300 },
  { h: 220, w: 220 },
];

function getRandomAspect() {
  return aspectRatios[Math.floor(Math.random() * aspectRatios.length)];
}

export default function StorePage() {
  const [artworks, setArtworks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    getArtworks().then(res => setArtworks(res.data || [])).catch(() => setError('Failed to load artworks')).finally(() => setLoading(false));
  }, []);
  return (
    <Container maxWidth="xl" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Artworks</Typography>
      {loading && <CircularProgress />}
      {error && <Alert severity="error">{error}</Alert>}
      <Grid container spacing={2}>
        {artworks.map((art, idx) => {
          const { h, w } = getRandomAspect();
          return (
            <Grid item key={art.id} xs={12} sm={6} md={4} lg={3}>
              <Paper sx={{ p: 1, height: h, width: w, overflow: 'hidden', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                {art.image_url && <img src={art.image_url} alt={art.title} style={{ maxWidth: '100%', maxHeight: '70%', objectFit: 'cover', borderRadius: 8 }} />}
                <Typography variant="subtitle1" sx={{ mt: 1 }}>{art.title}</Typography>
              </Paper>
            </Grid>
          );
        })}
      </Grid>
    </Container>
  );
} 