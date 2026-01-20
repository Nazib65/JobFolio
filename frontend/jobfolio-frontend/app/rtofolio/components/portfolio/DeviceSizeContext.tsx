"use client"

import { createContext, useContext } from "react"

type DeviceSize = "desktop" | "tablet" | "phone" | null

const DeviceSizeContext = createContext<DeviceSize>(null)

export const DeviceSizeProvider = DeviceSizeContext.Provider

export const useDeviceSize = () => {
    return useContext(DeviceSizeContext)
}
