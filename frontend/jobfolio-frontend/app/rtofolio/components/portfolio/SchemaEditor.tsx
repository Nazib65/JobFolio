"use client";

import { useEffect, useState } from "react";
import type { PortfolioSchema } from "@/types/portfolio";

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

  const inputClass =
    "w-full rounded-md border border-border bg-background px-3 py-2 text-sm";
  const labelClass = "text-xs font-medium uppercase tracking-wide";

  return (
    <div className="flex h-full flex-col gap-6 p-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold">Schema Editor</h2>
          <p className="text-xs text-muted-foreground">
            Update the basic fields and save to refresh the preview.
          </p>
        </div>
        <button
          className="rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground disabled:opacity-50"
          onClick={() => onSave(draft)}
          disabled={isSaving}
        >
          {isSaving ? "Saving..." : "Save changes"}
        </button>
      </div>

      <section className="space-y-3">
        <h3 className="text-base font-semibold">Theme</h3>
        <label className={labelClass}>Style</label>
        <input
          className={inputClass}
          value={(draft.theme as any)?.style ?? ""}
          onChange={(e) => updateTheme("style", e.target.value)}
        />
        <label className={labelClass}>Color palette</label>
        <input
          className={inputClass}
          value={(draft.theme as any)?.colorPalette ?? ""}
          onChange={(e) => updateTheme("colorPalette", e.target.value)}
        />
        <label className={labelClass}>Font</label>
        <input
          className={inputClass}
          value={(draft.theme as any)?.font ?? ""}
          onChange={(e) => updateTheme("font", e.target.value)}
        />
        <label className={labelClass}>Tone</label>
        <input
          className={inputClass}
          value={(draft.theme as any)?.tone ?? ""}
          onChange={(e) => updateTheme("tone", e.target.value)}
        />
      </section>

      {navbar && (
        <section className="space-y-3">
          <h3 className="text-base font-semibold">Navbar</h3>
          <label className={labelClass}>Name</label>
          <input
            className={inputClass}
            value={navbar?.props?.name ?? ""}
            onChange={(e) => updateSectionProps("navbar", "name", e.target.value)}
          />
          <label className={labelClass}>Logo URL</label>
          <input
            className={inputClass}
            value={navbar?.props?.logo ?? ""}
            onChange={(e) => updateSectionProps("navbar", "logo", e.target.value)}
          />
          <label className={labelClass}>CTA label</label>
          <input
            className={inputClass}
            value={navbar?.props?.cta_label ?? ""}
            onChange={(e) =>
              updateSectionProps("navbar", "cta_label", e.target.value)
            }
          />
          <label className={labelClass}>CTA URL</label>
          <input
            className={inputClass}
            value={navbar?.props?.cta_url ?? ""}
            onChange={(e) => updateSectionProps("navbar", "cta_url", e.target.value)}
          />
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className={labelClass}>Links</span>
              <button
                className="text-xs text-primary"
                onClick={() =>
                  addSectionPropListItem("navbar", "links", { label: "", url: "" })
                }
                type="button"
              >
                Add link
              </button>
            </div>
            {(navbar?.props?.links ?? []).map((link: any, idx: number) => (
              <div key={idx} className="space-y-2 rounded-md border p-2">
                <input
                  className={inputClass}
                  placeholder="Label"
                  value={link?.label ?? ""}
                  onChange={(e) =>
                    updateSectionPropListItem("navbar", "links", idx, "label", e.target.value)
                  }
                />
                <input
                  className={inputClass}
                  placeholder="URL"
                  value={link?.url ?? ""}
                  onChange={(e) =>
                    updateSectionPropListItem("navbar", "links", idx, "url", e.target.value)
                  }
                />
                <button
                  className="text-xs text-destructive"
                  onClick={() => removeSectionPropListItem("navbar", "links", idx)}
                  type="button"
                >
                  Remove link
                </button>
              </div>
            ))}
          </div>
        </section>
      )}

      {hero && (
        <section className="space-y-3">
          <h3 className="text-base font-semibold">Hero</h3>
          <label className={labelClass}>Name</label>
          <input
            className={inputClass}
            value={hero?.props?.name ?? ""}
            onChange={(e) => updateSectionProps("hero", "name", e.target.value)}
          />
          <label className={labelClass}>Hero text</label>
          <textarea
            className={inputClass}
            value={hero?.props?.hero_text ?? ""}
            onChange={(e) =>
              updateSectionProps("hero", "hero_text", e.target.value)
            }
          />
          <label className={labelClass}>CTA label</label>
          <input
            className={inputClass}
            value={hero?.props?.cta_label ?? ""}
            onChange={(e) => updateSectionProps("hero", "cta_label", e.target.value)}
          />
          <label className={labelClass}>CTA URL</label>
          <input
            className={inputClass}
            value={hero?.props?.cta_url ?? ""}
            onChange={(e) => updateSectionProps("hero", "cta_url", e.target.value)}
          />
          <label className={labelClass}>Hero image URL</label>
          <input
            className={inputClass}
            value={hero?.props?.image ?? ""}
            onChange={(e) => updateSectionProps("hero", "image", e.target.value)}
          />
        </section>
      )}

      {skills && (
        <section className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold">Skills</h3>
            <button
              className="text-xs text-primary"
              onClick={() => addSectionItem("skills", { name: "", icon: "" })}
              type="button"
            >
              Add skill
            </button>
          </div>
          {(skills?.items ?? []).map((skill: any, idx: number) => (
            <div key={idx} className="space-y-2 rounded-md border p-2">
              <input
                className={inputClass}
                placeholder="Skill name"
                value={skill?.name ?? ""}
                onChange={(e) =>
                  updateSectionItem("skills", idx, "name", e.target.value)
                }
              />
              <input
                className={inputClass}
                placeholder="Icon URL"
                value={skill?.icon ?? ""}
                onChange={(e) =>
                  updateSectionItem("skills", idx, "icon", e.target.value)
                }
              />
              <button
                className="text-xs text-destructive"
                onClick={() => removeSectionItem("skills", idx)}
                type="button"
              >
                Remove skill
              </button>
            </div>
          ))}
        </section>
      )}

      {experience && (
        <section className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold">Experience</h3>
            <button
              className="text-xs text-primary"
              onClick={() =>
                addSectionItem("experience", {
                  role: "",
                  company: "",
                  date: "",
                  description: "",
                })
              }
              type="button"
            >
              Add experience
            </button>
          </div>
          {(experience?.items ?? []).map((exp: any, idx: number) => (
            <div key={idx} className="space-y-2 rounded-md border p-2">
              <input
                className={inputClass}
                placeholder="Role"
                value={exp?.role ?? ""}
                onChange={(e) =>
                  updateSectionItem("experience", idx, "role", e.target.value)
                }
              />
              <input
                className={inputClass}
                placeholder="Company"
                value={exp?.company ?? ""}
                onChange={(e) =>
                  updateSectionItem("experience", idx, "company", e.target.value)
                }
              />
              <input
                className={inputClass}
                placeholder="Date range"
                value={exp?.date ?? ""}
                onChange={(e) =>
                  updateSectionItem("experience", idx, "date", e.target.value)
                }
              />
              <textarea
                className={inputClass}
                placeholder="Description"
                value={exp?.description ?? ""}
                onChange={(e) =>
                  updateSectionItem(
                    "experience",
                    idx,
                    "description",
                    e.target.value
                  )
                }
              />
              <button
                className="text-xs text-destructive"
                onClick={() => removeSectionItem("experience", idx)}
                type="button"
              >
                Remove experience
              </button>
            </div>
          ))}
        </section>
      )}

      {projects && (
        <section className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold">Projects</h3>
            <button
              className="text-xs text-primary"
              onClick={() =>
                addSectionItem("projects", {
                  title: "",
                  description: "",
                  image: "",
                  linkButton: "",
                })
              }
              type="button"
            >
              Add project
            </button>
          </div>
          {(projects?.items ?? []).map((project: any, idx: number) => (
            <div key={idx} className="space-y-2 rounded-md border p-2">
              <input
                className={inputClass}
                placeholder="Title"
                value={project?.title ?? ""}
                onChange={(e) =>
                  updateSectionItem("projects", idx, "title", e.target.value)
                }
              />
              <textarea
                className={inputClass}
                placeholder="Description"
                value={project?.description ?? ""}
                onChange={(e) =>
                  updateSectionItem("projects", idx, "description", e.target.value)
                }
              />
              <input
                className={inputClass}
                placeholder="Image URL"
                value={project?.image ?? ""}
                onChange={(e) =>
                  updateSectionItem("projects", idx, "image", e.target.value)
                }
              />
              <input
                className={inputClass}
                placeholder="Link URL"
                value={project?.linkButton ?? ""}
                onChange={(e) =>
                  updateSectionItem("projects", idx, "linkButton", e.target.value)
                }
              />
              <button
                className="text-xs text-destructive"
                onClick={() => removeSectionItem("projects", idx)}
                type="button"
              >
                Remove project
              </button>
            </div>
          ))}
        </section>
      )}

      {footer && (
        <section className="space-y-3">
          <h3 className="text-base font-semibold">Footer</h3>
          <label className={labelClass}>Name</label>
          <input
            className={inputClass}
            value={footer?.props?.name ?? ""}
            onChange={(e) => updateSectionProps("footer", "name", e.target.value)}
          />
          <label className={labelClass}>Logo URL</label>
          <input
            className={inputClass}
            value={footer?.props?.logo ?? ""}
            onChange={(e) => updateSectionProps("footer", "logo", e.target.value)}
          />
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className={labelClass}>Links</span>
              <button
                className="text-xs text-primary"
                onClick={() =>
                  addSectionPropListItem("footer", "links", { label: "", url: "" })
                }
                type="button"
              >
                Add link
              </button>
            </div>
            {(footer?.props?.links ?? []).map((link: any, idx: number) => (
              <div key={idx} className="space-y-2 rounded-md border p-2">
                <input
                  className={inputClass}
                  placeholder="Label"
                  value={link?.label ?? ""}
                  onChange={(e) =>
                    updateSectionPropListItem("footer", "links", idx, "label", e.target.value)
                  }
                />
                <input
                  className={inputClass}
                  placeholder="URL"
                  value={link?.url ?? ""}
                  onChange={(e) =>
                    updateSectionPropListItem("footer", "links", idx, "url", e.target.value)
                  }
                />
                <button
                  className="text-xs text-destructive"
                  onClick={() => removeSectionPropListItem("footer", "links", idx)}
                  type="button"
                >
                  Remove link
                </button>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

export default SchemaEditor;
