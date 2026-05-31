import type { CampaignProfile } from "./profile";

export const DRIVER_SKILLS = [
  {
    id: "smooth_inputs",
    name: "Smooth Inputs",
    requiredXp: 30,
    description: "Slightly improves tire grip through calmer steering."
  },
  {
    id: "brake_discipline",
    name: "Brake Discipline",
    requiredXp: 70,
    description: "Improves braking control for license trials."
  },
  {
    id: "racecraft_instinct",
    name: "Racecraft Instinct",
    requiredXp: 120,
    description: "Extra reputation from proven event wins."
  }
] as const;

export type DriverSkillId = (typeof DRIVER_SKILLS)[number]["id"];

export function unlockedDriverSkills(profile: CampaignProfile): DriverSkillId[] {
  return DRIVER_SKILLS.filter((skill) => profile.driverXp >= skill.requiredXp).map((skill) => skill.id);
}

export function driverGripBonus(profile: CampaignProfile): number {
  return unlockedDriverSkills(profile).includes("smooth_inputs") ? 0.04 : 0;
}

export function driverBrakeBonus(profile: CampaignProfile): number {
  return unlockedDriverSkills(profile).includes("brake_discipline") ? 0.05 : 0;
}
