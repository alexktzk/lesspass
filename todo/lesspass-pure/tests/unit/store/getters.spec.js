import * as getters from "@/store/getters";

test("passwordURL", () => {
  const state = {
    password: {
      login: "test@example.org",
      site: "example.org",
      uppercase: true,
      lowercase: true,
      digits: true,
      symbols: false,
      length: 16,
      counter: 1,
      version: 2
    },
    settings: {
      baseURL: "https://api.lesspass.com"
    }
  };

  expect(getters.passwordURL(state)).toBe(
    "https://www.lesspass.com/#/?passwordProfileEncoded=eyJsb2dpbiI6InRlc3RAZXhhbXBsZS5vcmciLCJzaXRlIjoiZXhhbXBsZS5vcmciLCJ1cHBlcmNhc2UiOnRydWUsImxvd2VyY2FzZSI6dHJ1ZSwiZGlnaXRzIjp0cnVlLCJzeW1ib2xzIjpmYWxzZSwibGVuZ3RoIjoxNiwiY291bnRlciI6MSwidmVyc2lvbiI6Mn0%3D"
  );
});

test("passwordURL encode uri component", () => {
  const state = {
    password: {
      login: "contact@lesspass.com"
    },
    settings: {
      baseURL: "https://api.lesspass.com"
    }
  };

  expect(getters.passwordURL(state)).toBe(
    "https://www.lesspass.com/#/?passwordProfileEncoded=eyJsb2dpbiI6ImNvbnRhY3RAbGVzc3Bhc3MuY29tIn0%3D"
  );
});

test("isAuthenticated", () => {
  const state = {
    isAuthenticated: true
  };
  expect(getters.isAuthenticated(state)).toBe(true);
  expect(getters.isGuest(state)).toBe(false);
});

test("isGuest", () => {
  const state = {
    isAuthenticated: false
  };
  expect(getters.isAuthenticated(state)).toBe(false);
  expect(getters.isGuest(state)).toBe(true);
});

test("shouldAutoFillSite", () => {
  expect(
    getters.shouldAutoFillSite({
      settings: {
        noAutoFillSite: true
      }
    })
  ).toBe(false);
  expect(
    getters.shouldAutoFillSite({
      settings: {
        noAutoFillSite: false
      }
    })
  ).toBe(true);
});

test("shouldRemoveSubdomain", () => {
  expect(
    getters.shouldRemoveSubdomain({
      settings: {
        removeSiteSubdomain: true
      }
    })
  ).toBe(true);
  expect(
    getters.shouldRemoveSubdomain({
      settings: {
        removeSiteSubdomain: false
      }
    })
  ).toBe(false);
});
