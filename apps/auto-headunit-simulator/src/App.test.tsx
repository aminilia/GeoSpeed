import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { App } from "./App";

describe("Auto head unit simulator", () => {
  it("renders navigation, signals, debug, and launch readiness", () => {
    render(<App />);

    expect(screen.getByText("Partner Head Unit Simulator")).toBeInTheDocument();
    expect(screen.getByText("Vehicle Signals")).toBeInTheDocument();
    expect(screen.getByText("Partner Debug")).toBeInTheDocument();
    expect(screen.getByText("Launch Readiness")).toBeInTheDocument();
    expect(screen.getByText("ADAS speed mismatch: cruise-control set speed exceeds posted limit.")).toBeInTheDocument();
  });
});

