const request = async (path, options = {}) => {
  const response = await fetch(path, { headers: { 'Content-Type': 'application/json', ...(options.headers || {}) }, ...options });
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try { const data = await response.json(); message = data.detail || message; } catch {}
    throw new Error(message);
  }
  return response.json();
};
export const getTickets = (filters = {}) => {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => value && params.set(key, value));
  return request(`/api/tickets?${params.toString()}`);
};
export const getDashboard = () => request('/api/dashboard');
export const createTicket = (payload) => request('/api/tickets', { method: 'POST', body: JSON.stringify(payload) });
export const updateStatus = (id, status) => request(`/api/tickets/${id}/status`, { method: 'PATCH', body: JSON.stringify({ status }) });
export const resetDemo = () => request('/api/demo/reset', { method: 'POST' });
