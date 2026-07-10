-- Run this in Supabase SQL Editor before running any Python script

create table if not exists daily_movers (
  id bigserial primary key,
  trade_date date not null,
  symbol text not null,
  close_price numeric,
  prev_close numeric,
  pct_change numeric,
  volume bigint,
  category text check (category in ('gainer', 'loser')),
  created_at timestamptz default now(),
  unique(trade_date, symbol)
);

create index if not exists idx_daily_movers_date on daily_movers(trade_date);
create index if not exists idx_daily_movers_category on daily_movers(trade_date, category);

-- Enable Row Level Security + public read-only policy (Flutter app just reads)
alter table daily_movers enable row level security;

create policy "Allow public read access"
  on daily_movers for select
  using (true);
