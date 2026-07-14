import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { useCustomFetch } from "@/composables/customFetch";

describe("useCustomFetch", () => {
  beforeEach(() => {
    document.body.innerHTML =
      '<input name="csrfmiddlewaretoken" value="csrf-token" />';
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("preserves parsed backend error payload", async () => {
    vi.spyOn(global, "fetch").mockResolvedValue({
      ok: false,
      status: 400,
      text: async () => JSON.stringify({ status: 400, error: "Bad Request" }),
    });

    await expect(useCustomFetch("/api/internal/visit/", { method: "POST" })).rejects
      .toMatchObject({
        data: { status: 400, error: "Bad Request" },
      });
  });
});
