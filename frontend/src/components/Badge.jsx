export function PriorityBadge({ value }) { return <span className={`badge priority priority-${value.toLowerCase()}`}><i />{value}</span>; }
export function StatusBadge({ value }) { return <span className={`badge status status-${value.toLowerCase().replace(' ', '-')}`}>{value}</span>; }
