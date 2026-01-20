"use client";

import { useEffect, useState } from "react";
import type { PortfolioSchema } from "@/types/portfolio";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Trash2, Plus, Save, Sparkles } from "lucide-react";

type SchemaEditorProps = {
  schema: PortfolioSchema;
  isSaving?: boolean;
  onSave: (schema: PortfolioSchema) => void;
};

const SchemaEditor = ({ schema, isSaving, onSave }: SchemaEditorProps) => {
  const [draft, setDraft] = useState<PortfolioSchema | null>(null);

  useEffect(() => {
    setDraft(JSON.parse(JSON.stringify(schema)));
  }, [schema]);

  if (!draft) return null;

  const updateTheme = (key: string, value: string) => {
    setDraft((prev) => {
      if (!prev) return prev;
      return { ...prev, theme: { ...(prev.theme ?? {}), [key]: value } };
    });
  };

  const updateSectionProps = (type: string, key: string, value: string) => {
    setDraft((prev) => {
      if (!prev) return prev;
      const sections = (prev.sections as any[]).map((section) => {
        if (section?.type !== type) return section;
        return { ...section, props: { ...(section.props ?? {}), [key]: value } };
      });
      return { ...prev, sections };
    });
  };

  const updateSectionItem = (
    type: string,
    index: number,
    key: string,
    value: string
  ) => {
    setDraft((prev) => {
      if (!prev) return prev;
      const sections = (prev.sections as any[]).map((section) => {
        if (section?.type !== type) return section;
        const items = Array.isArray(section.items) ? [...section.items] : [];
        const item = { ...(items[index] ?? {}) };
        item[key] = value;
        items[index] = item;
        return { ...section, items };
      });
      return { ...prev, sections };
    });
  };

  const updateSectionPropListItem = (
    type: string,
    listKey: string,
    index: number,
    key: string,
    value: string
  ) => {
    setDraft((prev) => {
      if (!prev) return prev;
      const sections = (prev.sections as any[]).map((section) => {
        if (section?.type !== type) return section;
        const props = { ...(section.props ?? {}) };
        const list = Array.isArray(props[listKey]) ? [...props[listKey]] : [];
        const item = { ...(list[index] ?? {}) };
        item[key] = value;
        list[index] = item;
        props[listKey] = list;
        return { ...section, props };
      });
      return { ...prev, sections };
    });
  };

  const addSectionItem = (type: string, defaults: Record<string, any>) => {
    setDraft((prev) => {
      if (!prev) return prev;
      const sections = (prev.sections as any[]).map((section) => {
        if (section?.type !== type) return section;
        const items = Array.isArray(section.items) ? [...section.items] : [];
        items.push({ ...defaults });
        return { ...section, items };
      });
      return { ...prev, sections };
    });
  };

  const addSectionPropListItem = (
    type: string,
    listKey: string,
    defaults: Record<string, any>
  ) => {
    setDraft((prev) => {
      if (!prev) return prev;
      const sections = (prev.sections as any[]).map((section) => {
        if (section?.type !== type) return section;
        const props = { ...(section.props ?? {}) };
        const list = Array.isArray(props[listKey]) ? [...props[listKey]] : [];
        list.push({ ...defaults });
        props[listKey] = list;
        return { ...section, props };
      });
      return { ...prev, sections };
    });
  };

  const removeSectionItem = (type: string, index: number) => {
    setDraft((prev) => {
      if (!prev) return prev;
      const sections = (prev.sections as any[]).map((section) => {
        if (section?.type !== type) return section;
        const items = Array.isArray(section.items) ? [...section.items] : [];
        items.splice(index, 1);
        return { ...section, items };
      });
      return { ...prev, sections };
    });
  };

  const removeSectionPropListItem = (type: string, listKey: string, index: number) => {
    setDraft((prev) => {
      if (!prev) return prev;
      const sections = (prev.sections as any[]).map((section) => {
        if (section?.type !== type) return section;
        const props = { ...(section.props ?? {}) };
        const list = Array.isArray(props[listKey]) ? [...props[listKey]] : [];
        list.splice(index, 1);
        props[listKey] = list;
        return { ...section, props };
      });
      return { ...prev, sections };
    });
  };

  const findSection = (type: string) =>
    (draft.sections as any[])?.find((section) => section?.type === type) ?? null;

  const navbar = findSection("navbar");
  const hero = findSection("hero");
  const skills = findSection("skills");
  const experience = findSection("experience");
  const projects = findSection("projects");
  const footer = findSection("footer");

  return (
    <div className="flex h-full flex-col gap-6 p-6 bg-linear-to-br from-ui-background via-ui-background to-ui-muted/20 overflow-y-auto scrollbar-hide">
      {/* Header Section */}
      <Card className="border-ui-primary/10 shadow-lg hover:shadow-xl transition-all duration-300 bg-ui-card text-ui-card-foreground">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-ui-primary" />
                <CardTitle className="text-2xl">Schema Editor</CardTitle>
              </div>
              <CardDescription className="text-ui-muted-foreground">
                Update the basic fields and save to refresh the preview.
              </CardDescription>
            </div>
            <Button
              onClick={() => onSave(draft)}
              disabled={isSaving}
              size="lg"
              className="shadow-md hover:shadow-lg transition-all duration-300 bg-ui-primary text-ui-primary-foreground hover:bg-ui-primary/90"
            >
              <Save className="mr-2 h-4 w-4" />
              {isSaving ? "Saving..." : "Save changes"}
            </Button>
          </div>
        </CardHeader>
      </Card>

      {/* Theme Section */}
      <Card className="group hover:border-ui-primary/30 transition-all duration-300 shadow-inner bg-ui-card text-ui-card-foreground">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Badge variant="secondary" className="transition-all group-hover:scale-105 bg-ui-secondary text-ui-secondary-foreground">Theme</Badge>
            <CardTitle>Visual Settings</CardTitle>
          </div>
          <CardDescription className="text-ui-muted-foreground">Customize the look and feel of your portfolio</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="style" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Style</Label>
              <Input
                id="style"
                value={(draft.theme as any)?.style ?? ""}
                onChange={(e) => updateTheme("style", e.target.value)}
                placeholder="e.g., modern, minimal"
                className="border-ui-input bg-ui-background text-ui-foreground"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="colorPalette" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Color Palette</Label>
              <Input
                id="colorPalette"
                value={(draft.theme as any)?.colorPalette ?? ""}
                onChange={(e) => updateTheme("colorPalette", e.target.value)}
                placeholder="e.g., blue, dark"
                className="border-ui-input bg-ui-background text-ui-foreground"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="font" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Font</Label>
              <Input
                id="font"
                value={(draft.theme as any)?.font ?? ""}
                onChange={(e) => updateTheme("font", e.target.value)}
                placeholder="e.g., Inter, Roboto"
                className="border-ui-input bg-ui-background text-ui-foreground"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="tone" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Tone</Label>
              <Input
                id="tone"
                value={(draft.theme as any)?.tone ?? ""}
                onChange={(e) => updateTheme("tone", e.target.value)}
                placeholder="e.g., professional, casual"
                className="border-ui-input bg-ui-background text-ui-foreground"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Navbar Section */}
      {navbar && (
        <Card className="group hover:border-ui-primary/30 transition-all duration-300 shadow-inner bg-ui-card text-ui-card-foreground">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="transition-all group-hover:scale-105 bg-ui-secondary text-ui-secondary-foreground">Navbar</Badge>
              <CardTitle>Navigation Bar</CardTitle>
            </div>
            <CardDescription className="text-ui-muted-foreground">Configure your site's navigation</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="navbar-name" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Name</Label>
                <Input
                  id="navbar-name"
                  value={navbar?.props?.name ?? ""}
                  onChange={(e) => updateSectionProps("navbar", "name", e.target.value)}
                  placeholder="Your name"
                  className="border-ui-input bg-ui-background text-ui-foreground"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="navbar-logo" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Logo URL</Label>
                <Input
                  id="navbar-logo"
                  value={navbar?.props?.logo ?? ""}
                  onChange={(e) => updateSectionProps("navbar", "logo", e.target.value)}
                  placeholder="https://..."
                  className="border-ui-input bg-ui-background text-ui-foreground"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="navbar-cta-label" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">CTA Label</Label>
                <Input
                  id="navbar-cta-label"
                  value={navbar?.props?.cta_label ?? ""}
                  onChange={(e) => updateSectionProps("navbar", "cta_label", e.target.value)}
                  placeholder="Contact Me"
                  className="border-ui-input bg-ui-background text-ui-foreground"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="navbar-cta-url" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">CTA URL</Label>
                <Input
                  id="navbar-cta-url"
                  value={navbar?.props?.cta_url ?? ""}
                  onChange={(e) => updateSectionProps("navbar", "cta_url", e.target.value)}
                  placeholder="mailto:..."
                  className="border-ui-input bg-ui-background text-ui-foreground"
                />
              </div>
            </div>
            
            <div className="space-y-3 pt-4 border-t border-ui-border">
              <div className="flex items-center justify-between">
                <Label className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Links</Label>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => addSectionPropListItem("navbar", "links", { label: "", url: "" })}
                  type="button"
                  className="hover:scale-105 transition-transform border-ui-border hover:bg-ui-accent hover:text-ui-accent-foreground"
                >
                  <Plus className="mr-1 h-3 w-3" />
                  Add Link
                </Button>
              </div>
              <div className="space-y-3">
                {(navbar?.props?.links ?? []).map((link: any, idx: number) => (
                  <Card key={idx} className="p-4 hover:shadow-md transition-all duration-200 bg-ui-muted/30 border-ui-border">
                    <div className="space-y-3">
                      <Input
                        placeholder="Label"
                        value={link?.label ?? ""}
                        onChange={(e) =>
                          updateSectionPropListItem("navbar", "links", idx, "label", e.target.value)
                        }
                        className="border-ui-input bg-ui-background text-ui-foreground"
                      />
                      <Input
                        placeholder="URL"
                        value={link?.url ?? ""}
                        onChange={(e) =>
                          updateSectionPropListItem("navbar", "links", idx, "url", e.target.value)
                        }
                        className="border-ui-input bg-ui-background text-ui-foreground"
                      />
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => removeSectionPropListItem("navbar", "links", idx)}
                        type="button"
                        className="w-full hover:scale-105 transition-transform bg-ui-destructive text-ui-destructive-foreground hover:bg-ui-destructive/90"
                      >
                        <Trash2 className="mr-1 h-3 w-3" />
                        Remove Link
                      </Button>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Hero Section */}
      {hero && (
        <Card className="group hover:border-ui-primary/30 transition-all duration-300 shadow-inner bg-ui-card text-ui-card-foreground">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="transition-all group-hover:scale-105 bg-ui-secondary text-ui-secondary-foreground">Hero</Badge>
              <CardTitle>Hero Section</CardTitle>
            </div>
            <CardDescription className="text-ui-muted-foreground">Create a powerful first impression</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="hero-name" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Name</Label>
              <Input
                id="hero-name"
                value={hero?.props?.name ?? ""}
                onChange={(e) => updateSectionProps("hero", "name", e.target.value)}
                placeholder="Your name"
                className="border-ui-input bg-ui-background text-ui-foreground"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="hero-text" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Hero Text</Label>
              <Textarea
                id="hero-text"
                value={hero?.props?.hero_text ?? ""}
                onChange={(e) => updateSectionProps("hero", "hero_text", e.target.value)}
                placeholder="Your compelling tagline..."
                rows={4}
                className="border-ui-input bg-ui-background text-ui-foreground"
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="hero-cta-label" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">CTA Label</Label>
                <Input
                  id="hero-cta-label"
                  value={hero?.props?.cta_label ?? ""}
                  onChange={(e) => updateSectionProps("hero", "cta_label", e.target.value)}
                  placeholder="Get in touch"
                  className="border-ui-input bg-ui-background text-ui-foreground"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="hero-cta-url" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">CTA URL</Label>
                <Input
                  id="hero-cta-url"
                  value={hero?.props?.cta_url ?? ""}
                  onChange={(e) => updateSectionProps("hero", "cta_url", e.target.value)}
                  placeholder="#contact"
                  className="border-ui-input bg-ui-background text-ui-foreground"
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="hero-image" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Hero Image URL</Label>
              <Input
                id="hero-image"
                value={hero?.props?.image ?? ""}
                onChange={(e) => updateSectionProps("hero", "image", e.target.value)}
                placeholder="https://..."
                className="border-ui-input bg-ui-background text-ui-foreground"
              />
            </div>
          </CardContent>
        </Card>
      )}

      {/* Skills Section */}
      {skills && (
        <Card className="group hover:border-ui-primary/30 transition-all duration-300 shadow-inner bg-ui-card text-ui-card-foreground">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="transition-all group-hover:scale-105 bg-ui-secondary text-ui-secondary-foreground">Skills</Badge>
                  <CardTitle>Skills & Technologies</CardTitle>
                </div>
                <CardDescription className="text-ui-muted-foreground">Showcase your technical expertise</CardDescription>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => addSectionItem("skills", { name: "", icon: "" })}
                type="button"
                className="hover:scale-105 transition-transform border-ui-border hover:bg-ui-accent hover:text-ui-accent-foreground"
              >
                <Plus className="mr-1 h-3 w-3" />
                Add Skill
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            {(skills?.items ?? []).map((skill: any, idx: number) => (
              <Card key={idx} className="p-4 hover:shadow-md transition-all duration-200 bg-ui-muted/30 border-ui-border">
                <div className="space-y-3">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div className="space-y-2">
                      <Label className="text-xs text-ui-muted-foreground">Skill Name</Label>
                      <Input
                        placeholder="e.g., React, Python"
                        value={skill?.name ?? ""}
                        onChange={(e) =>
                          updateSectionItem("skills", idx, "name", e.target.value)
                        }
                        className="border-ui-input bg-ui-background text-ui-foreground"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label className="text-xs text-ui-muted-foreground">Icon URL</Label>
                      <Input
                        placeholder="https://..."
                        value={skill?.icon ?? ""}
                        onChange={(e) =>
                          updateSectionItem("skills", idx, "icon", e.target.value)
                        }
                        className="border-ui-input bg-ui-background text-ui-foreground"
                      />
                    </div>
                  </div>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => removeSectionItem("skills", idx)}
                    type="button"
                    className="w-full hover:scale-105 transition-transform bg-ui-destructive text-ui-destructive-foreground hover:bg-ui-destructive/90"
                  >
                    <Trash2 className="mr-1 h-3 w-3" />
                    Remove Skill
                  </Button>
                </div>
              </Card>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Experience Section */}
      {experience && (
        <Card className="group hover:border-ui-primary/30 transition-all duration-300 shadow-inner bg-ui-card text-ui-card-foreground">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="transition-all group-hover:scale-105 bg-ui-secondary text-ui-secondary-foreground">Experience</Badge>
                  <CardTitle>Work Experience</CardTitle>
                </div>
                <CardDescription className="text-ui-muted-foreground">Highlight your professional journey</CardDescription>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() =>
                  addSectionItem("experience", {
                    role: "",
                    company: "",
                    date: "",
                    description: "",
                  })
                }
                type="button"
                className="hover:scale-105 transition-transform border-ui-border hover:bg-ui-accent hover:text-ui-accent-foreground"
              >
                <Plus className="mr-1 h-3 w-3" />
                Add Experience
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            {(experience?.items ?? []).map((exp: any, idx: number) => (
              <Card key={idx} className="p-4 hover:shadow-md transition-all duration-200 bg-ui-muted/30 border-ui-border">
                <div className="space-y-3">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div className="space-y-2">
                      <Label className="text-xs text-ui-muted-foreground">Role</Label>
                      <Input
                        placeholder="Senior Developer"
                        value={exp?.role ?? ""}
                        onChange={(e) =>
                          updateSectionItem("experience", idx, "role", e.target.value)
                        }
                        className="border-ui-input bg-ui-background text-ui-foreground"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label className="text-xs text-ui-muted-foreground">Company</Label>
                      <Input
                        placeholder="Acme Inc."
                        value={exp?.company ?? ""}
                        onChange={(e) =>
                          updateSectionItem("experience", idx, "company", e.target.value)
                        }
                        className="border-ui-input bg-ui-background text-ui-foreground"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label className="text-xs text-ui-muted-foreground">Date Range</Label>
                    <Input
                      placeholder="Jan 2020 - Present"
                      value={exp?.date ?? ""}
                      onChange={(e) =>
                        updateSectionItem("experience", idx, "date", e.target.value)
                      }
                      className="border-ui-input bg-ui-background text-ui-foreground"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-xs text-ui-muted-foreground">Description</Label>
                    <Textarea
                      placeholder="Describe your responsibilities and achievements..."
                      value={exp?.description ?? ""}
                      onChange={(e) =>
                        updateSectionItem(
                          "experience",
                          idx,
                          "description",
                          e.target.value
                        )
                      }
                      rows={3}
                      className="border-ui-input bg-ui-background text-ui-foreground"
                    />
                  </div>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => removeSectionItem("experience", idx)}
                    type="button"
                    className="w-full hover:scale-105 transition-transform bg-ui-destructive text-ui-destructive-foreground hover:bg-ui-destructive/90"
                  >
                    <Trash2 className="mr-1 h-3 w-3" />
                    Remove Experience
                  </Button>
                </div>
              </Card>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Projects Section */}
      {projects && (
        <Card className="group hover:border-ui-primary/30 transition-all duration-300 shadow-inner bg-ui-card text-ui-card-foreground">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="transition-all group-hover:scale-105 bg-ui-secondary text-ui-secondary-foreground">Projects</Badge>
                  <CardTitle>Portfolio Projects</CardTitle>
                </div>
                <CardDescription className="text-ui-muted-foreground">Showcase your best work</CardDescription>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() =>
                  addSectionItem("projects", {
                    title: "",
                    description: "",
                    image: "",
                    linkButton: "",
                  })
                }
                type="button"
                className="hover:scale-105 transition-transform border-ui-border hover:bg-ui-accent hover:text-ui-accent-foreground"
              >
                <Plus className="mr-1 h-3 w-3" />
                Add Project
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            {(projects?.items ?? []).map((project: any, idx: number) => (
              <Card key={idx} className="p-4 hover:shadow-md transition-all duration-200 bg-ui-muted/30 border-ui-border">
                <div className="space-y-3">
                  <div className="space-y-2">
                    <Label className="text-xs text-ui-muted-foreground">Title</Label>
                    <Input
                      placeholder="Project name"
                      value={project?.title ?? ""}
                      onChange={(e) =>
                        updateSectionItem("projects", idx, "title", e.target.value)
                      }
                      className="border-ui-input bg-ui-background text-ui-foreground"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-xs text-ui-muted-foreground">Description</Label>
                    <Textarea
                      placeholder="Describe your project..."
                      value={project?.description ?? ""}
                      onChange={(e) =>
                        updateSectionItem("projects", idx, "description", e.target.value)
                      }
                      rows={3}
                      className="border-ui-input bg-ui-background text-ui-foreground"
                    />
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div className="space-y-2">
                      <Label className="text-xs text-ui-muted-foreground">Image URL</Label>
                      <Input
                        placeholder="https://..."
                        value={project?.image ?? ""}
                        onChange={(e) =>
                          updateSectionItem("projects", idx, "image", e.target.value)
                        }
                        className="border-ui-input bg-ui-background text-ui-foreground"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label className="text-xs text-ui-muted-foreground">Link URL</Label>
                      <Input
                        placeholder="https://..."
                        value={project?.linkButton ?? ""}
                        onChange={(e) =>
                          updateSectionItem("projects", idx, "linkButton", e.target.value)
                        }
                        className="border-ui-input bg-ui-background text-ui-foreground"
                      />
                    </div>
                  </div>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => removeSectionItem("projects", idx)}
                    type="button"
                    className="w-full hover:scale-105 transition-transform bg-ui-destructive text-ui-destructive-foreground hover:bg-ui-destructive/90"
                  >
                    <Trash2 className="mr-1 h-3 w-3" />
                    Remove Project
                  </Button>
                </div>
              </Card>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Footer Section */}
      {footer && (
        <Card className="group hover:border-ui-primary/30 transition-all duration-300 shadow-inner bg-ui-card text-ui-card-foreground">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="transition-all group-hover:scale-105 bg-ui-secondary text-ui-secondary-foreground">Footer</Badge>
              <CardTitle>Footer Section</CardTitle>
            </div>
            <CardDescription className="text-ui-muted-foreground">Complete your portfolio footer</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="footer-name" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Name</Label>
                <Input
                  id="footer-name"
                  value={footer?.props?.name ?? ""}
                  onChange={(e) => updateSectionProps("footer", "name", e.target.value)}
                  placeholder="Your name"
                  className="border-ui-input bg-ui-background text-ui-foreground"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="footer-logo" className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Logo URL</Label>
                <Input
                  id="footer-logo"
                  value={footer?.props?.logo ?? ""}
                  onChange={(e) => updateSectionProps("footer", "logo", e.target.value)}
                  placeholder="https://..."
                  className="border-ui-input bg-ui-background text-ui-foreground"
                />
              </div>
            </div>
            
            <div className="space-y-3 pt-4 border-t border-ui-border">
              <div className="flex items-center justify-between">
                <Label className="text-ui-muted-foreground uppercase text-xs font-semibold tracking-wide">Links</Label>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => addSectionPropListItem("footer", "links", { label: "", url: "" })}
                  type="button"
                  className="hover:scale-105 transition-transform border-ui-border hover:bg-ui-accent hover:text-ui-accent-foreground"
                >
                  <Plus className="mr-1 h-3 w-3" />
                  Add Link
                </Button>
              </div>
              <div className="space-y-3">
                {(footer?.props?.links ?? []).map((link: any, idx: number) => (
                  <Card key={idx} className="p-4 hover:shadow-md transition-all duration-200 bg-ui-muted/30 border-ui-border">
                    <div className="space-y-3">
                      <Input
                        placeholder="Label"
                        value={link?.label ?? ""}
                        onChange={(e) =>
                          updateSectionPropListItem("footer", "links", idx, "label", e.target.value)
                        }
                        className="border-ui-input bg-ui-background text-ui-foreground"
                      />
                      <Input
                        placeholder="URL"
                        value={link?.url ?? ""}
                        onChange={(e) =>
                          updateSectionPropListItem("footer", "links", idx, "url", e.target.value)
                        }
                        className="border-ui-input bg-ui-background text-ui-foreground"
                      />
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => removeSectionPropListItem("footer", "links", idx)}
                        type="button"
                        className="w-full hover:scale-105 transition-transform bg-ui-destructive text-ui-destructive-foreground hover:bg-ui-destructive/90"
                      >
                        <Trash2 className="mr-1 h-3 w-3" />
                        Remove Link
                      </Button>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default SchemaEditor;
