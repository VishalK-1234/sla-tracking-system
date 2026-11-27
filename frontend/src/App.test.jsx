import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App.jsx';

const tickets = [{id:1,title:'VPN access unavailable',description:'VPN is down',requester:'Maya Chen',priority:'High',status:'Open',created_at:'2026-11-27T10:00:00Z',due_at:'2026-11-28T10:00:00Z',is_overdue:false,sla_hours:24,hours_remaining:20}];
const dash = {total:1,open:1,in_progress:0,resolved:0,overdue:0,sla_compliance:100};
beforeEach(() => { vi.restoreAllMocks(); global.fetch = vi.fn(async (url) => ({ok:true,json:async()=> url.includes('/dashboard') ? dash : tickets})); });

describe('SLA Desk dashboard', () => {
  it('renders dashboard metrics and ticket list', async () => {
    render(<App/>);
    expect(await screen.findByText('VPN access unavailable')).toBeInTheDocument();
    expect(screen.getByText('SLA compliance')).toBeInTheDocument();
    expect(screen.getByText('Total tickets')).toBeInTheDocument();
  });
  it('opens the create ticket form', async () => {
    const user = userEvent.setup(); render(<App/>);
    await user.click(screen.getAllByRole('button', {name:/create ticket/i})[0]);
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByLabelText('Ticket title')).toBeInTheDocument();
    expect(screen.getByText(/48 hour SLA/i)).toBeInTheDocument();
  });
});
