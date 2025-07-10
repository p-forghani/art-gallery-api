import React, { useEffect, useState } from 'react';
import { getArtistDashboard, createArtwork, updateArtwork, deleteArtwork } from './api';
import { Container, Typography, Grid, Paper, TextField, Button, Box, IconButton, Dialog, DialogTitle, DialogContent, DialogActions, CircularProgress, Alert } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

export default function ArtistPage() {
  const [artworks, setArtworks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ title: '', description: '', image_url: '' });
  const [editId, setEditId] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  const fetchArtworks = () => {
    setLoading(true);
    getArtistDashboard().then(setArtworks).catch(() => setError('Failed to load artworks')).finally(() => setLoading(false));
  };

  useEffect(() => { fetchArtworks(); }, []);

  const handleChange = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }));

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      if (editId) {
        await updateArtwork(editId, form);
      } else {
        await createArtwork(form);
      }
      setForm({ title: '', description: '', image_url: '' });
      setEditId(null);
      setDialogOpen(false);
      fetchArtworks();
    } catch {
      setError('Failed to save artwork');
    }
  };

  const handleEdit = art => {
    setForm({ title: art.title, description: art.description, image_url: art.image_url || '' });
    setEditId(art.id);
    setDialogOpen(true);
  };

  const handleDelete = async id => {
    if (window.confirm('Delete this artwork?')) {
      await deleteArtwork(id);
      fetchArtworks();
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Artist Artworks</Typography>
      <Button variant="contained" sx={{ mb: 2 }} onClick={() => { setEditId(null); setForm({ title: '', description: '', image_url: '' }); setDialogOpen(true); }}>Add Artwork</Button>
      {error && <Alert severity="error">{error}</Alert>}
      {loading ? <CircularProgress /> : (
        <Grid container spacing={2}>
          {artworks.map(art => (
            <Grid item xs={12} sm={6} md={4} key={art.id}>
              <Paper sx={{ p: 2, position: 'relative' }}>
                <Typography variant="h6">{art.title}</Typography>
                <Typography variant="body2">{art.description}</Typography>
                {art.image_url && <img src={art.image_url} alt={art.title} style={{ width: '100%', marginTop: 8 }} />}
                <Box sx={{ position: 'absolute', top: 8, right: 8 }}>
                  <IconButton onClick={() => handleEdit(art)}><EditIcon /></IconButton>
                  <IconButton onClick={() => handleDelete(art.id)}><DeleteIcon /></IconButton>
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
        <DialogTitle>{editId ? 'Edit Artwork' : 'Add Artwork'}</DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            <TextField label="Title" name="title" fullWidth margin="normal" value={form.title} onChange={handleChange} required />
            <TextField label="Description" name="description" fullWidth margin="normal" value={form.description} onChange={handleChange} required />
            <TextField label="Image URL" name="image_url" fullWidth margin="normal" value={form.image_url} onChange={handleChange} />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
            <Button type="submit" variant="contained">Save</Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
} 