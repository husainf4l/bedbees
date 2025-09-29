import { apiService } from './api';

class UploadService {
  async uploadFile(file: File): Promise<string> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      // Use fetch directly for file uploads since apiService doesn't handle FormData
      const token = localStorage.getItem('accessToken');
      const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:3333/api';
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        headers: token ? {
          'Authorization': `Bearer ${token}`,
        } : {},
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed. Please try again.');
      }

      const result = await response.json();
      return result.url;
    } catch (error) {
      console.error('Upload failed:', error);
      // Fallback: create a local blob URL for preview purposes
      // In production, this should be replaced with actual backend upload
      return URL.createObjectURL(file);
    }
  }

  async uploadMultipleFiles(files: File[]): Promise<string[]> {
    const uploadPromises = files.map(file => this.uploadFile(file));
    return Promise.all(uploadPromises);
  }
}

export const uploadService = new UploadService();