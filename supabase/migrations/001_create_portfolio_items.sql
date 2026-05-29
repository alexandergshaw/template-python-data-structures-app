-- Migration: Create portfolio_items table
-- This migration sets up the core portfolio table with Row Level Security.
-- Run this in the Supabase SQL editor or via the Supabase CLI.

-- =============================================================================
-- TABLE: portfolio_items
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.portfolio_items (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    slug        text UNIQUE NOT NULL,
    student_name text NOT NULL,
    title       text NOT NULL,
    summary     text NOT NULL DEFAULT '',
    project_url text NOT NULL DEFAULT '#',
    created_at  timestamptz NOT NULL DEFAULT now(),
    updated_at  timestamptz NOT NULL DEFAULT now()
);

-- Add an index on slug for fast lookups
CREATE INDEX IF NOT EXISTS idx_portfolio_items_slug
    ON public.portfolio_items (slug);

-- Add an index on created_at for ordered listing
CREATE INDEX IF NOT EXISTS idx_portfolio_items_created_at
    ON public.portfolio_items (created_at DESC);

-- =============================================================================
-- ROW LEVEL SECURITY (RLS)
-- =============================================================================
-- Enable RLS on the table
ALTER TABLE public.portfolio_items ENABLE ROW LEVEL SECURITY;

-- Policy: Allow public (anon) read access to all portfolio items.
-- This is appropriate for a public portfolio site.
CREATE POLICY "Allow public read access"
    ON public.portfolio_items
    FOR SELECT
    TO anon, authenticated
    USING (true);

-- Policy: Only authenticated users with service_role can insert/update/delete.
-- In practice, use the service_role key in admin contexts only.
CREATE POLICY "Allow service_role full access"
    ON public.portfolio_items
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- =============================================================================
-- TRIGGER: Auto-update updated_at on row modification
-- =============================================================================
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON public.portfolio_items
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();

-- =============================================================================
-- SEED DATA (optional — remove for production)
-- =============================================================================
-- INSERT INTO public.portfolio_items (slug, student_name, title, summary, project_url)
-- VALUES
--     ('example-project', 'Jane Doe', 'My Capstone Project', 'A brief summary of the project.', 'https://github.com/janedoe/capstone');
