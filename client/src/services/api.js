import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getConversations = async () => {
    const response = await api.get('/conversations');
    return response.data;
};

export const createConversation = async () => {
    const response = await api.post('/conversations');
    return response.data;
};

export const getConversation = async (id) => {
    const response = await api.get(`/conversations/${id}`);
    return response.data;
};

export const deleteConversation = async (id) => {
    const response = await api.delete(`/conversations/${id}`);
    return response.data;
};

export const sendMessage = async (messageData) => {
    const response = await api.post('/messages', messageData);
    return response.data;
};

export const getMessages = async (conversationId) => {
    const response = await api.get(`/messages/conversation/${conversationId}`);
    return response.data;
};

export const uploadAudio = async (file, messageId) => {
    const formData = new FormData();
    formData.append('file', file);
    if (messageId) {
        formData.append('message_id', messageId);
    }
    const response = await api.post('/audio/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const getAudioUrl = (filename) => {
    return `${API_URL}/audio/${filename}`;
};

export const searchConversations = async (query) => {
    const response = await api.get('/search', { params: { q: query } });
    return response.data;
};

export const createSummary = async (conversationId) => {
    const response = await api.post(`/summary/conversations/${conversationId}`);
    return response.data;
};

export const getSummary = async (conversationId) => {
    const response = await api.get(`/summary/conversations/${conversationId}`);
    return response.data;
};

export const getLanguages = async () => {
    const response = await api.get('/languages');
    return response.data;
};

export default api;
