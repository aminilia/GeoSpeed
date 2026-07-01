import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { App } from "./App";

vi.mock("maplibre-gl", () => {
  class MapMock {
    addControl = vi.fn();
    addSource = vi.fn();
    addLayer = vi.fn();
    remove = vi.fn();

    on(eventName: string, _layerOrHandler: unknown, maybeHandler?: unknown) {
      if (eventName === "load") {
        const handler = typeof _layerOrHandler === "function" ? _layerOrHandler : maybeHandler;
        if (typeof handler === "function") {
          handler();
        }
      }
      return this;
    }
  }

  class MarkerMock {
    setLngLat() {
      return this;
    }

    setPopup() {
      return this;
    }

    addTo() {
      return this;
    }
  }

  class PopupMock {
    setText() {
      return this;
    }
  }

  class NavigationControlMock {}

  return {
    default: {
      Map: MapMock,
      Marker: MarkerMock,
      Popup: PopupMock,
      NavigationControl: NavigationControlMock
    }
  };
});

describe("App", () => {
  it("renders the overview dashboard", () => {
    render(<App />);

    expect(screen.getByText("GeoSpeed AI")).toBeInTheDocument();
    expect(screen.getByText("Network Confidence")).toBeInTheDocument();
    expect(screen.getAllByText("Release Readiness").length).toBeGreaterThan(0);
  });

  it("navigates to map explorer and renders the map", () => {
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "Map Explorer" }));

    expect(screen.getByText("Map Layers")).toBeInTheDocument();
    expect(screen.getByTestId("map-container")).toBeInTheDocument();
  });

  it("renders quality issues page", () => {
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "Quality Issues" }));

    expect(screen.getByText("Quality Work Queue")).toBeInTheDocument();
    expect(screen.getByText("Sign-to-road heading mismatch")).toBeInTheDocument();
  });
});
