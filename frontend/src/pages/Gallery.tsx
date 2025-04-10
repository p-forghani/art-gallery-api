import React from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Container,
  Card,
  CardMedia,
  CardContent,
  Typography,
  Box,
  Button,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import { storeService } from '../services/api';

interface Artwork {
  id: string;
  name: string;
  description: string;
  price: string;
  image_path?: string;
  image_url?: string;
}

const BACKEND_URL = 'http://localhost:8000';

const Gallery: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));

  const { data: artworks, isLoading, error } = useQuery<Artwork[]>({
    queryKey: ['artworks'],
    queryFn: storeService.getArtworks,
  });

  // Helper function to get the full image URL
  const getImageUrl = (artwork: Artwork) => {
    const path = artwork.image_path || artwork.image_url;
    if (!path) return '';
    
    // Handle the renamed file
    if (path.includes('final-fantasy-vii-rebirth-aerith-gainsborough-vc-2880x1800.jpg')) {
      return `${BACKEND_URL}/uploads/final-fantasy.jpg`;
    }
    
    if (path.startsWith('http')) {
      // Extract filename from full URL
      const filename = path.split('/').pop();
      return `${BACKEND_URL}/uploads/${filename}`;
    }
    return `${BACKEND_URL}${path}`;
  };

  if (isLoading) {
    return (
      <Container maxWidth="lg" sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h4" color="primary">
          Loading...
        </Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h4" color="error">
          Error loading artworks
        </Typography>
      </Container>
    );
  }

  return (
    <Box sx={{ backgroundColor: 'background.default', minHeight: '100vh', py: 8 }}>
      <Container maxWidth="lg">
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography
            variant="h1"
            component="h1"
            gutterBottom
            sx={{
              color: 'primary.main',
              fontWeight: 700,
              mb: 2,
            }}
          >
            Art Gallery
          </Typography>
          <Typography
            variant="h5"
            color="text.secondary"
            sx={{
              maxWidth: '600px',
              mx: 'auto',
              mb: 4,
            }}
          >
            Discover and explore our collection of unique artworks
          </Typography>
        </Box>

        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: {
              xs: '1fr',
              sm: 'repeat(2, 1fr)',
              md: 'repeat(3, 1fr)',
            },
            gap: 4,
          }}
        >
          {artworks?.map((artwork) => (
            <Box key={artwork.id}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: theme.shadows[8],
                  },
                }}
              >
                <CardMedia
                  component="img"
                  height={isMobile ? 200 : isTablet ? 250 : 300}
                  image={getImageUrl(artwork)}
                  alt={artwork.name}
                  sx={{
                    objectFit: 'cover',
                    borderTopLeftRadius: 8,
                    borderTopRightRadius: 8,
                  }}
                />
                <CardContent sx={{ flexGrow: 1, p: 3 }}>
                  <Typography
                    gutterBottom
                    variant="h5"
                    component="div"
                    sx={{
                      fontWeight: 600,
                      color: 'primary.main',
                      mb: 2,
                    }}
                  >
                    {artwork.name}
                  </Typography>
                  <Typography
                    variant="body1"
                    color="text.secondary"
                    sx={{
                      mb: 3,
                      minHeight: '60px',
                    }}
                  >
                    {artwork.description}
                  </Typography>
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      mt: 'auto',
                    }}
                  >
                    <Typography
                      variant="h6"
                      color="secondary.main"
                      sx={{ fontWeight: 700 }}
                    >
                      ${artwork.price}
                    </Typography>
                    <Button
                      variant="contained"
                      color="primary"
                      sx={{
                        borderRadius: 2,
                        px: 3,
                        py: 1,
                      }}
                    >
                      View Details
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Box>
          ))}
        </Box>
      </Container>
    </Box>
  );
};

export default Gallery; 