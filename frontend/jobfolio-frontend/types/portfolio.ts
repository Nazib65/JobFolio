// Columns are numeric counts in the JSON (e.g. desktop: 1)
export type Columns = {
    desktop: number;
    mobile: number;
};

// A slot may be defined as a detailed object or just a string identifier
export type Slot = {
    name: string;
    optional?: boolean;
    type?: string;
};

// Slots map used in responsive desktop/mobile layout variants
export type SlotsMap = Record<string, (Slot | string)[] | string | null>;

// Responsive config used under `desktop` / `mobile` keys in some layouts
export type ResponsiveConfig = {
    type: string;
    gap?: string | null;
    align?: string | null;
    justify?: string | null;
    slots?: SlotsMap | null;
    // allow additional arbitrary keys (flexible schema coming from backend)
    [key: string]: any;
};

export type Theme = {
    width?: string;
    maxWidth?: string;
    margin?: string;
    display?: string;
    flexDirection?: string | null;
    alignItems?: string;
    colorPalette?: string;
    font?: string | null;
}


export type PortfolioSchema = {

    schemaVersion? : string | null;
    theme : Theme;
    sections : [];
};

// General layout that covers both simple and responsive shapes
export type Layout = {
    type?: string;
    direction?: string | null;
    gap?: string | null;
    columns?: Columns | null;
    desktop?: ResponsiveConfig | null;
    mobile?: ResponsiveConfig | null;
    width?: string | null;
    maxWidth?: string | null;
    margin?: string | null
    [key: string]: any;
};

export type Constraints = {
    maxWidth?: string | null;
};

export type ItemLayout = {
    type?: string;
    layout?: Layout | null;
    slots?: Slot[] | null;
    constraints?: Constraints | null;
};

// Project item shape based on provided JSON
export type ProjectItem = {
    id?: string;
    title?: string;
    description?: string;
    image?: string | null;
    linkButton?: string | null; // JSON uses `linkButton`
    // accept legacy or alternative field names
    link?: string | null;
    [key: string]: any;
};

export type Projects = {
    priority?: string | null;
    layout?: Layout | null;
    itemLayout?: ItemLayout | null;
    items?: ProjectItem[] | null;
};

// Specific props for the `hero` section (note: key with dash is allowed)
export type HeroProps = {
    name?: string | null;
    "hero-text"?: string | null;
    CTA?: string | null;
    image?: string | null;
    [key: string]: any;
};

export type Hero = {
    type: "hero";
    priority?: string | null;
    layout?: Layout | null;
    props?: HeroProps | null;
    items?: null;
    itemLayout?: null;
};

