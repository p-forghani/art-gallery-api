import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
} from '@mui/material';
import { adminService } from '../services/api';

const Admin: React.FC = () => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!image) {
      setMessage({ type: 'error', text: 'Please select an image' });
      return;
    }

    const formData = new FormData();
    formData.append('name', name);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('image', image);

    try {
      await adminService.uploadArtwork(formData);
      setMessage({ type: 'success', text: 'Artwork uploaded successfully' });
      setName('');
      setDescription('');
      setPrice('');
      setImage(null);
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to upload artwork' });
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Upload Artwork
          </Typography>
          {message && (
            <Alert severity={message.type} sx={{ mb: 2 }}>
              {message.text}
            </Alert>
          )}
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              margin="normal"
              required
              multiline
              rows={4}
            />
            <TextField
              fullWidth
              label="Price"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              margin="normal"
              required
              type="number"
            />
            <Button
              variant="contained"
              component="label"
              fullWidth
              sx={{ mt: 2 }}
            >
              Upload Image
              <input
                type="file"
                hidden
                accept="image/*"
                onChange={(e) => setImage(e.target.files?.[0] || null)}
              />
            </Button>
            {image && (
              <Typography variant="body2" sx={{ mt: 1 }}>
                Selected: {image.name}
              </Typography>
            )}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              sx={{ mt: 3 }}
            >
              Upload Artwork
            </Button>
          </form>
        </Paper>
      </Box>
    </Container>
  );
};

export default Admin; 