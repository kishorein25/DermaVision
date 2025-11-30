import { useState, useEffect } from 'react';

export interface Doctor {
  id: number;
  name: string;
  specialization: string;
  experience: string;
  location: string;
  rating: number;
  image: string;
  available: boolean;
  phone: string;
  email: string;
}

export const MOCK_DOCTORS: Doctor[] = [
  {
    id: 1,
    name: "Dr. Kishore S",
    specialization: "Dermatologist (MD)",
    experience: "12 Years",
    location: "India",
    rating: 4.9,
    image: "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&q=80&w=300&h=300",
    available: true,
    phone: "8220411874",
    email: "ks6700822@gmail.com",
  },
  {
    id: 2,
    name: "Dr. Liwis Nishanth A",
    specialization: "Cosmetic Dermatologist",
    experience: "0 Years",
    location: "India",
    rating: 4.7,
    image: "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&q=80&w=300&h=300",
    available: true,
    phone: "9943397972",
    email: "liwisnishanth2023@gmail.com",
  },
];

export interface DiseaseTip {
  id: string;
  name: string;
  description: string;
  causes: string[];
  tipsMen: string[];
  tipsWomen: string[];
  whenToSeeDoctor: string;
}

export const DISEASE_TIPS: Record<string, DiseaseTip> = {
  "acne": {
    id: "acne",
    name: "Acne Vulgaris",
    description: "A common skin condition that occurs when hair follicles become plugged with oil and dead skin cells.",
    causes: ["Excess oil (sebum) production", "Hair follicles clogged by oil and dead skin cells", "Bacteria", "Inflammation"],
    tipsMen: ["Wash face twice daily with mild cleanser", "Shave carefully with sharp blade", "Avoid oily hair products"],
    tipsWomen: ["Use non-comedogenic makeup", "Remove makeup before sleeping", "Keep hair clean and off the face"],
    whenToSeeDoctor: "If self-care remedies don't clear your acne, or the acne is severe (cysts/nodules) leaving scars."
  },
  "eczema": {
    id: "eczema",
    name: "Eczema (Atopic Dermatitis)",
    description: "A condition that makes your skin red and itchy. It's common in children but can occur at any age.",
    causes: ["Immune system activation", "Genetics", "Environmental triggers", "Stress"],
    tipsMen: ["Use lukewarm water for showers", "Apply moisturizer immediately after bathing", "Wear soft fabrics like cotton"],
    tipsWomen: ["Avoid harsh soaps and detergents", "Moisturize frequently", "Manage stress levels"],
    whenToSeeDoctor: "If you are so uncomfortable that the condition is affecting sleep and daily activities, or if you have a skin infection."
  },
  "psoriasis": {
    id: "psoriasis",
    name: "Psoriasis",
    description: "A skin disease that causes a rash with itchy, scaly patches, most commonly on the knees, elbows, trunk and scalp.",
    causes: ["Immune system problem", "Genetics", "Infections", "Stress", "Cold weather"],
    tipsMen: ["Limit alcohol consumption", "Use moisturizing soaps", "Quit smoking"],
    tipsWomen: ["Use heavy creams or ointments", "Get moderate sunlight exposure", "Avoid skin injuries"],
    whenToSeeDoctor: "If psoriasis becomes severe or widespread, or causes you discomfort and pain."
  }
};

export interface HistoryItem {
  id: number;
  date: string;
  prediction: string;
  severity: "Mild" | "Moderate" | "Severe";
  image?: string;
}

export const MOCK_HISTORY: HistoryItem[] = [
  { id: 1, date: "2024-05-10T10:30:00", prediction: "Acne", severity: "Mild" },
  { id: 2, date: "2024-04-22T14:15:00", prediction: "Eczema", severity: "Moderate" },
  { id: 3, date: "2024-03-15T09:00:00", prediction: "Healthy Skin", severity: "Mild" }
];
