export const inr = (n) =>
  '₹' + Number(n || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })

export const pct = (n) => `${Number(n || 0).toFixed(1)}%`

export const timeAgo = (dateStr) => {
  if (!dateStr) return '—'
  const days = Math.floor((Date.now() - new Date(dateStr)) / 86400000)
  if (days <= 0) return 'today'
  if (days === 1) return 'yesterday'
  if (days < 30) return `${days}d ago`
  if (days < 365) return `${Math.floor(days / 30)}mo ago`
  return `${Math.floor(days / 365)}y ago`
}

export function StatusBadge({ status }) {
  const map = {
    completed: ['badge-green', null],
    running: ['badge-amber', true],
    draft: ['badge-gray', null],
    failed: ['badge-red', null],
    delivered: ['badge-green', null],
    sent: ['badge-teal', null],
    queued: ['badge-gray', null],
    opened: ['badge-teal', null],
    read: ['badge-teal', null],
    clicked: ['badge-amber', null],
    converted: ['badge-green', null],
  }
  const [cls, pulse] = map[status] || ['badge-gray', null]
  return (
    <span className={`badge ${cls}`}>
      {pulse && <span className="pulse-dot" />}
      {status}
    </span>
  )
}

export function TagBadge({ tag }) {
  const map = {
    vip: 'badge-amber',
    loyal: 'badge-green',
    new: 'badge-teal',
    'at-risk': 'badge-red',
    lapsed: 'badge-gray',
    'weekend-visitor': 'badge-teal',
  }
  return <span className={`badge ${map[tag] || 'badge-gray'}`}>{tag}</span>
}

export function ChannelBadge({ channel }) {
  return <span className="badge badge-teal" style={{ textTransform: 'uppercase', letterSpacing: '0.05em' }}>{channel}</span>
}

export function Loader() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: 40 }}>
      <div className="spinner" />
    </div>
  )
}
