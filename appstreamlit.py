import streamlit as st
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# 1 load dataset
#@st.cache_data
def load_dataset():
    ds = xr.open_dataset('cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m_1773955220875.nc')
    #monthly
    sst_monthly = ds['thetao'].resample(time='1MS').mean().load()
    return sst_monthly

# 2 plot function
def plot_monthly(data_bulan, nama_bulan):
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    p = data_bulan.plot.contourf(
        ax=ax,
        transform=ccrs.PlateCarree(),
        levels=100,
        cmap='turbo',
        add_colorbar=False,
        #vmin=vmin,
        #vmax=vmax,
        extend='both'
    )

    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.COASTLINE)
    ax.set_extent([95, 141, -10.5, 6])

    gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.3)
    gl.top_labels = False
    gl.right_labels = False

    plt.colorbar(p, orientation='horizontal', pad=0.08, label='SST (°C)', format='%.2f')
    plt.title(f'2025 SST Monthly - {nama_bulan}', fontsize=15)

    return fig

# 3 UI Streamlit
st.set_page_config(page_title="SST Visualization", layout="wide")
st.title("Visualisasi Suhu Permukaan Laut (SST)")

#Sidebar
st.sidebar.header("Pengaturan Visualisasi")
month_idx = st.sidebar.selectbox("Pilih Bulan", options=list(range(1, 13)), index=0)
#vmin = st.sidebar.slider("VMin Global", value=27.5)
#vmax = st.sidebar.slider("VMax Global", value=31.5)

#load data
with st.spinner("Memuat data..."):
    sst_monthly = load_dataset()

#runnin plot
month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
data_bulan = sst_monthly.sel(time=sst_monthly['time.month'] == month_idx).isel(depth=0)

if len(data_bulan.time) > 1:
    data_bulan = data_bulan.mean(dim='time')
else:
    data_bulan = data_bulan.squeeze()

fig_hasil = plot_monthly(data_bulan, month_names[month_idx-1])

#tampilkan
st.pyplot(fig_hasil)
