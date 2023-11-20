import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { $api } from "../../http";
import { ITourCard, Tour } from "../../@types";

interface MyKnownError {
  errorMessage: string;
}

export const getTours = createAsyncThunk<
  { data: Tour[]; types: string[] },
  number | undefined,
  { rejectValue: MyKnownError }
  // @ts-ignore
>("tours", async (limit, { rejectWithValue }) => {
  try {
    const { data } = await $api("tour/TourAdd", {
      params: {
        [limit ? "limit" : ""]: limit,
      },
    });

    if (!data.results.length)
      return rejectWithValue({ errorMessage: "There is nothing here yet." });

    let types: string[] = [];

    data.results?.forEach(
      (tour: ITourCard) => !types.includes(tour.type) && types.push(tour.type)
    );

    return { data: data.results, types };
  } catch (e) {
    if (e instanceof Error) return rejectWithValue({ errorMessage: e.message });
  }
});

interface ToursSliceState {
  status: "" | "loading" | "success" | "error";
  message: string;
  data: Tour[];
  types: string[];
}

const initialState: ToursSliceState = {
  status: "",
  message: "",
  data: [],
  types: [],
};

const toursSlice = createSlice({
  name: "toursSlice",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(getTours.pending, (state) => {
      state.status = "loading";
    });
    builder.addCase(getTours.fulfilled, (state, action) => {
      state.data = action.payload.data;
      state.types = action.payload.types;
      state.status = "success";
    });
    builder.addCase(getTours.rejected, (state, action) => {
      state.status = "error";
      // @ts-ignore
      state.message = action.payload?.errorMessage || "";
    });
  },
});

export default toursSlice.reducer;
