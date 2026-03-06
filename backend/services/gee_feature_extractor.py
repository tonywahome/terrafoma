"""
Google Earth Engine feature extraction for real-time biomass estimation.
Extracts the same features used for training the biomass model.
"""

import ee
import logging
from typing import Dict, Optional, List
import numpy as np

logger = logging.getLogger(__name__)

# Initialize EE once at module load
try:
    ee.Initialize()
    logger.info("Google Earth Engine initialized successfully")
except Exception as e:
    logger.warning(f"EE initialization failed: {e}")


def calculate_indices(image: ee.Image) -> ee.Image:
    """
    Calculate vegetation indices from Sentinel-2 bands.
    Same indices as used in training data.
    """
    # NDVI
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('ndvi')
    
    # EVI
    evi = image.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
        {
            'NIR': image.select('B8'),
            'RED': image.select('B4'),
            'BLUE': image.select('B2')
        }
    ).rename('evi')
    
    # SAVI (L=0.5)
    savi = image.expression(
        '((NIR - RED) / (NIR + RED + 0.5)) * 1.5',
        {
            'NIR': image.select('B8'),
            'RED': image.select('B4')
        }
    ).rename('savi')
    
    # NDMI
    ndmi = image.normalizedDifference(['B8', 'B11']).rename('ndmi')
    
    # NBR
    nbr = image.normalizedDifference(['B8', 'B12']).rename('nbr')
    
    return image.addBands([ndvi, evi, savi, ndmi, nbr])


def extract_sentinel_features(
    geometry: Dict,
    start_date: str = "2023-01-01",
    end_date: str = "2024-12-31",
    scale: int = 10
) -> Optional[Dict]:
    """
    Extract Sentinel-2 features for a geometry.
    
    Args:
        geometry: GeoJSON geometry (Point or Polygon)
        start_date: Start date for imagery (YYYY-MM-DD)
        end_date: End date for imagery (YYYY-MM-DD)
        scale: Spatial resolution in meters (default 10m)
        
    Returns:
        Dictionary with 13 features matching training data:
        {blue, green, red, nir, swir1, swir2, ndvi, evi, savi, ndmi, nbr, elevation, slope}
    """
    try:
        # Convert GeoJSON to EE geometry
        if geometry['type'] == 'Point':
            coords = geometry['coordinates']
            ee_geometry = ee.Geometry.Point(coords)
            region = ee_geometry.buffer(50)  # 50m buffer for point
        elif geometry['type'] == 'Polygon':
            coords = geometry['coordinates']
            ee_geometry = ee.Geometry.Polygon(coords)
            region = ee_geometry
        else:
            logger.error(f"Unsupported geometry type: {geometry['type']}")
            return None
        
        # Get Sentinel-2 collection
        collection = (
            ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
            .filterBounds(ee_geometry)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
            .map(calculate_indices)
        )
        
        # Check if images available
        count = collection.size().getInfo()
        if count == 0:
            logger.warning(f"No Sentinel-2 images found for geometry")
            return None
        
        logger.info(f"Found {count} cloud-free Sentinel-2 images")
        
        # Create median composite
        composite = collection.median()
        
        # Extract spectral bands and indices
        bands_to_extract = [
            'B2', 'B3', 'B4', 'B8', 'B11', 'B12',  # Spectral bands
            'ndvi', 'evi', 'savi', 'ndmi', 'nbr'    # Vegetation indices
        ]
        
        # Sample the composite
        sample = composite.select(bands_to_extract).reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=scale,
            maxPixels=1e9
        ).getInfo()
        
        # Get terrain data from SRTM
        dem = ee.Image('USGS/SRTMGL1_003')
        elevation = dem.select('elevation').reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=30,
            maxPixels=1e9
        ).getInfo()['elevation']
        
        # Calculate slope
        slope = ee.Terrain.slope(dem).reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=30,
            maxPixels=1e9
        ).getInfo()['slope']
        
        # Convert to feature vector matching training data
        # Order: blue, green, red, nir, swir1, swir2, ndvi, evi, savi, ndmi, nbr, elevation, slope
        features = {
            'blue': sample.get('B2'),
            'green': sample.get('B3'),
            'red': sample.get('B4'),
            'nir': sample.get('B8'),
            'swir1': sample.get('B11'),
            'swir2': sample.get('B12'),
            'ndvi': sample.get('ndvi'),
            'evi': sample.get('evi'),
            'savi': sample.get('savi'),
            'ndmi': sample.get('ndmi'),
            'nbr': sample.get('nbr'),
            'elevation': elevation,
            'slope': slope,
            'n_images': count
        }
        
        # Check for missing values
        if any(v is None for k, v in features.items() if k != 'n_images'):
            logger.error(f"Missing values in extracted features: {features}")
            return None
        
        logger.info(f"Successfully extracted features: NDVI={features['ndvi']:.3f}, Elevation={features['elevation']:.1f}m")
        return features
        
    except Exception as e:
        logger.error(f"Error extracting features: {e}")
        return None


def features_to_array(features: Dict) -> np.ndarray:
    """
    Convert feature dictionary to numpy array in correct order for model.
    
    Args:
        features: Dictionary with feature names and values
        
    Returns:
        1D numpy array with 13 features in training order
    """
    feature_order = [
        'blue', 'green', 'red', 'nir', 'swir1', 'swir2',
        'ndvi', 'evi', 'savi', 'ndmi', 'nbr',
        'elevation', 'slope'
    ]
    
    return np.array([features[name] for name in feature_order])
