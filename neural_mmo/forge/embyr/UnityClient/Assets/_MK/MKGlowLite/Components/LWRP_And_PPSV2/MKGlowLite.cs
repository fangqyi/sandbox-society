//////////////////////////////////////////////////////
// MK Glow PostProcessing Stack     	            //
//					                                //
// Created by Michael Kremmel                       //
// www.michaelkremmel.de                            //
// Copyright © 2019 All rights reserved.            //
//////////////////////////////////////////////////////
//#if UNITY_POST_PROCESSING_STACK_V2
using System;
using UnityEngine;
using UnityEngine.Rendering.PostProcessing;
using System.Collections;
using System.Collections.Generic;

namespace MK.Glow.LWRP
{
    [Serializable]
    [PostProcess(typeof(MKGlowLiteRenderer), PostProcessEvent.BeforeStack, "MK/MKGlowLite")]
    public sealed class MKGlowLite : PostProcessEffectSettings
    {
        [System.Serializable]
        public sealed class Texture2DParameter : ParameterOverride<Texture2D>
        {
            public override void Interp(Texture2D from, Texture2D to, float t)
            {
                value = t > 0 ? to : from;
            }
        }

        [System.Serializable]
        public sealed class DebugViewParameter : ParameterOverride<MK.Glow.DebugView>
        {
            public override void Interp(MK.Glow.DebugView from, MK.Glow.DebugView to, float t)
            {
                value = t > 0 ? to : from;
            }
        }

        [System.Serializable]
        public sealed class WorkflowParameter : ParameterOverride<MK.Glow.Workflow>
        {
            public override void Interp(MK.Glow.Workflow from, MK.Glow.Workflow to, float t)
            {
                value = t > 0 ? to : from;
            }
        }

        [System.Serializable]
        public sealed class LayerMaskParameter : ParameterOverride<LayerMask>
        {
            public override void Interp(LayerMask from, LayerMask to, float t)
            {
                value = t > 0 ? to : from;
            }
        }

        [System.Serializable]
        public sealed class MinMaxRangeParameter : ParameterOverride<MK.Glow.MinMaxRange>
        {
            public override void Interp(MK.Glow.MinMaxRange from, MK.Glow.MinMaxRange to, float t)
            {
                value.minValue = Mathf.Lerp(from.minValue, to.minValue, t);
                value.maxValue = Mathf.Lerp(from.maxValue, to.maxValue, t);
            }
        }

        #if UNITY_EDITOR && !UNITY_CLOUD_BUILD
        public bool showEditorMainBehavior = true;
		public bool showEditorBloomBehavior;
		public bool showEditorLensSurfaceBehavior;
        /// <summary>
        /// Keep this value always untouched, editor internal only
        /// </summary>
        public bool isInitialized = false;
        #endif
        
        //Main
        public DebugViewParameter debugView = new DebugViewParameter() { value = MK.Glow.DebugView.None };
        public WorkflowParameter workflow = new WorkflowParameter() { value = MK.Glow.Workflow.Threshold };
        public LayerMaskParameter selectiveRenderLayerMask = new LayerMaskParameter() { value = -1 };
        [Range(-1f, 1f)]
        public FloatParameter anamorphicRatio = new FloatParameter() { value = 0 };

        //Bloom
        [MK.Glow.MinMaxRange(0, 10)]
        public MinMaxRangeParameter bloomThreshold = new MinMaxRangeParameter() { value = new MinMaxRange(1.25f, 10f) };
        [Range(1f, 10f)]
		public FloatParameter bloomScattering = new FloatParameter() { value = 7f };
		public FloatParameter bloomIntensity = new FloatParameter() { value = 0f };

        //LensSurface
        public BoolParameter allowLensSurface = new BoolParameter() { overrideState = true, value = false };
		public Texture2DParameter lensSurfaceDirtTexture = new Texture2DParameter();
		public FloatParameter lensSurfaceDirtIntensity = new FloatParameter() { value = 0.0f };
		public Texture2DParameter lensSurfaceDiffractionTexture = new Texture2DParameter();
		public FloatParameter lensSurfaceDiffractionIntensity = new FloatParameter() { value = 0.0f };

        public override bool IsEnabledAndSupported(PostProcessRenderContext context)
        {
            if(workflow == Workflow.Selective && PipelineProperties.xrEnabled)
                return false;
            else
                return Compatibility.IsSupported;
        }

        /*
        /// <summary>
        /// Load some mobile optimized settings
        /// </summary>
        //[ContextMenu("Load Preset For Mobile")]
        internal void LoadMobilePreset()
        {
            bloomScattering.value = 5f;
            renderPriority.value = RenderPriority.Performance;
            quality.value = Quality.Low;
            allowGlare.value = false;
            allowLensFlare.value = false;
            lensFlareScattering.value = 5;
            allowLensSurface.value = false;
        }

        /// <summary>
        /// Load some quality optimized settings
        /// </summary>
        //[ContextMenu("Load Preset For Quality")]
        internal void LoadQualityPreset()
        {
            bloomScattering.value = 7f;
            renderPriority.value = RenderPriority.Quality;
            quality.value = Quality.High;
            allowGlare.value = false;
            allowLensFlare.value = false;
            lensFlareScattering.value = 6;
            allowLensSurface.value = false;
        }
        */
    }
    
    public sealed class MKGlowLiteRenderer : PostProcessEffectRenderer<MKGlowLite>
    {
		private Effect effect = new Effect();
        private RenderTarget _source, _destination;

        public override void Init()
        {
            effect.Enable(RenderPipeline.SRP);
        }

        public override void Release()
        {
            effect.Disable();
        }

        public override void Render(PostProcessRenderContext context)
        {
            context.command.BeginSample(PipelineProperties.CommandBufferProperties.commandBufferName);
            _source.renderTargetIdentifier = context.source;
            _destination.renderTargetIdentifier = context.destination;
            SettingsPPSV2 settings = this.settings;
            LWRP.CameraDataPPSv2 cameraData = context.camera;
			effect.Build(_source, _destination, settings, context.command, cameraData, context.camera);
            context.command.EndSample(PipelineProperties.CommandBufferProperties.commandBufferName);
        }
    }
}
//#endif